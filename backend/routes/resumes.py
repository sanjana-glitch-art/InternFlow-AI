from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional
import json
import os

router = APIRouter()

# Simple file-based storage for the hackathon
STORAGE_FILE = "data/resumes.json"

def load_resumes():
    if not os.path.exists(STORAGE_FILE):
        return {"base_resumes": [], "company_resumes": []}
    with open(STORAGE_FILE, "r") as f:
        return json.load(f)

def save_resumes(data):
    os.makedirs("data", exist_ok=True)
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=2)

class ResumeBase(BaseModel):
    name: str          # e.g. "ML Engineer Resume"
    content: str       # raw resume text
    tags: list[str] = []  # e.g. ["ML", "Data Science"]

class CompanyResume(BaseModel):
    company: str       # e.g. "Google"
    job_title: str     # e.g. "ML Intern"
    base_resume_name: str
    tailored_content: str

@router.get("/")
def get_all_resumes():
    return load_resumes()

@router.post("/base")
def add_base_resume(resume: ResumeBase):
    data = load_resumes()
    resume_dict = resume.dict()
    resume_dict["id"] = f"base-{len(data['base_resumes']) + 1}"
    data["base_resumes"].append(resume_dict)
    save_resumes(data)
    return {"message": "Resume saved!", "resume": resume_dict}

@router.post("/company")
def add_company_resume(resume: CompanyResume):
    data = load_resumes()
    resume_dict = resume.dict()
    resume_dict["id"] = f"company-{len(data['company_resumes']) + 1}"
    data["company_resumes"].append(resume_dict)
    save_resumes(data)
    return {"message": "Company resume saved!", "resume": resume_dict}

@router.delete("/base/{resume_id}")
def delete_base_resume(resume_id: str):
    data = load_resumes()
    data["base_resumes"] = [r for r in data["base_resumes"] if r["id"] != resume_id]
    save_resumes(data)
    return {"message": "Deleted!"}
@router.delete("/company/{resume_id}")
def delete_company_resume(resume_id: str):
    data = load_resumes()
    data["company_resumes"] = [r for r in data["company_resumes"] if r["id"] != resume_id]
    save_resumes(data)
    return {"message": "Deleted!"}
