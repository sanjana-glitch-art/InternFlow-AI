import requests
import os
import time
from fastapi import APIRouter

router = APIRouter()

# ── Adzuna API config ─────────────────────────────────────────────────────────
# Get free keys at: https://developer.adzuna.com/
# Set these in your .env or environment before running:
ADZUNA_APP_ID= "1bc8845f"
ADZUNA_APP_KEY="5e2a982115defeb4f65fd12857ff240c"
#ADZUNA_APP_ID  = os.getenv("ADZUNA_APP_ID",  "")
#ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "")
ADZUNA_BASE    = "https://api.adzuna.com/v1/api/jobs/us/search"

# ── SimplifyJobs fallback (used if Adzuna keys not set) ───────────────────────
# Points to the NEW 2025/2026 repo — not the stale Summer2025 one
SIMPLIFY_URLS = [
    "https://raw.githubusercontent.com/SimplifyJobs/New-Grad-Positions/dev/.github/scripts/listings.json",
    "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/.github/scripts/listings.json",
    "https://raw.githubusercontent.com/SimplifyJobs/Summer2025-Internships/dev/.github/scripts/listings.json",
]

# Simple in-process cache: {cache_key: (timestamp, data)}
_cache: dict = {}
CACHE_TTL = 300  # 5 minutes


def _cached(key, fn):
    now = time.time()
    if key in _cache and now - _cache[key][0] < CACHE_TTL:
        return _cache[key][1]
    result = fn()
    _cache[key] = (now, result)
    return result


# ── Adzuna fetcher ────────────────────────────────────────────────────────────
def fetch_adzuna(search: str, location: str, limit: int) -> list:
    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:
        return []

    # Build query — combine search + location into what param
    what = search if search else "internship"
    if "intern" not in what.lower():
        what = f"{what} internship"

    params = {
        "app_id":        ADZUNA_APP_ID,
        "app_key":       ADZUNA_APP_KEY,
        "results_per_page": min(limit, 50),
        "what":          what,
        "sort_by":       "date",          # newest first — critical
        "content-type":  "application/json",
    }
    if location:
        params["where"] = location

    try:
        resp = requests.get(f"{ADZUNA_BASE}/1", params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        jobs = []
        for r in data.get("results", []):
            jobs.append({
                "id":          r.get("id", ""),
                "title":       r.get("title", ""),
                "company":     r.get("company", {}).get("display_name", "Unknown"),
                "locations":   [r.get("location", {}).get("display_name", "")],
                "url":         r.get("redirect_url", "#"),
                "date_posted": r.get("created", ""),
                "sponsorship": "Unknown",
                "terms":       [],
                "description": r.get("description", "No description available."),
                "source":      "adzuna",
            })
        return jobs
    except Exception as e:
        print(f"[Adzuna error] {e}")
        return []


# ── SimplifyJobs fetcher ──────────────────────────────────────────────────────
def fetch_simplify() -> list:
    for url in SIMPLIFY_URLS:
        try:
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                # Filter only active listings
                active = [j for j in data if j.get("active", True)]
                # Sort newest first (date_posted is a Unix timestamp)
                active.sort(key=lambda j: j.get("date_posted", 0), reverse=True)
                print(f"[SimplifyJobs] loaded {len(active)} active from {url}")
                return active
        except Exception as e:
            print(f"[SimplifyJobs] failed {url}: {e}")
            continue
    return []


def get_simplify_cached() -> list:
    return _cached("simplify", fetch_simplify)


# ── Search helper ─────────────────────────────────────────────────────────────
def matches(job: dict, search: str, location: str) -> bool:
    """
    True if the job matches the search query.
    Checks title, company, description, AND terms — not just title.
    Each word in the query must appear somewhere in the combined text.
    """
    if not search and not location:
        return True

    title       = job.get("title", "").lower()
    company     = (job.get("company") or job.get("company_name", "")).lower()
    description = job.get("description", "").lower()
    terms       = " ".join(job.get("terms", [])).lower()
    combined    = f"{title} {company} {description} {terms}"

    if search:
        # Every word in the query must hit somewhere in the combined text
        for word in search.lower().split():
            if word not in combined:
                return False

    if location:
        locs = " ".join(job.get("locations", [])).lower()
        if location.lower() not in locs:
            return False

    return True


def normalize(job: dict) -> dict:
    """Normalize SimplifyJobs shape to our standard shape."""
    company = job.get("company_name") or job.get("company") or "Unknown"
    title   = job.get("title", "")
    return {
        "id":          f"{company}-{title}".replace(" ", "-").lower()[:80],
        "title":       title,
        "company":     company,
        "locations":   job.get("locations", []),
        "url":         job.get("url", "#"),
        "date_posted": job.get("date_posted", 0),
        "sponsorship": job.get("sponsorship", "Unknown"),
        "terms":       job.get("terms", []),
        "description": job.get("description", "No description available."),
        "source":      "simplify",
    }


# ── Route ─────────────────────────────────────────────────────────────────────
@router.get("/")
def get_jobs(search: str = "", location: str = "", limit: int = 50):
    jobs = []

    # 1. Try Adzuna first (live, keyword-matched, date-sorted by API)
    if ADZUNA_APP_ID and ADZUNA_APP_KEY:
        jobs = fetch_adzuna(search, location, limit)

    # 2. Fall back to SimplifyJobs if Adzuna not configured or returned nothing
    if not jobs:
        raw = get_simplify_cached()
        normalized = [normalize(j) for j in raw]
        jobs = [j for j in normalized if matches(j, search, location)]
        # Already sorted newest-first from fetch_simplify()

    # 3. Always slice to limit
    jobs = jobs[:limit]

    return {"jobs": jobs, "total": len(jobs)}
