
import uuid

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Resume, User
from app.dependencies import get_current_user

from app.services.resume_parser import parse_resume_text
from app.services.job_matcher import calculate_job_match
from app.services.ats_checker import evaluate_ats
from app.services.career_recommender import recommend_careers
from app.services.learning_roadmap import generate_learning_roadmap
from app.services.interview_preparer import prepare_interview
from app.services.report_generator import generate_pdf_report


router = APIRouter(
    prefix="/reports",
    tags=["PDF Report Generation"]
)

REPORT_DIR = Path("reports")


class ReportRequest(BaseModel):

    resume_id: int = Field(gt=0)

    job_title: str = Field(
        min_length=2,
        max_length=150
    )

    job_description: str = Field(
        min_length=30,
        max_length=15000
    )

    target_role: str = Field(
        min_length=2,
        max_length=150
    )


@router.post("/generate", response_class=FileResponse)
def create_career_report(

    data: ReportRequest,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    # Find user's own resume
    resume = db.query(Resume).filter(
        Resume.id == data.resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    if not resume.extracted_text:
        raise HTTPException(
            status_code=422,
            detail="Resume text is empty"
        )

    try:

        # Parse resume
        parsed = parse_resume_text(
            resume.extracted_text
        )

        candidate_skills = parsed["technical_skills"]

        # Job matching
        matching = calculate_job_match(
            resume.extracted_text,
            data.job_description
        )

        # ATS analysis
        ats = evaluate_ats(
            resume.extracted_text,
            data.job_description
        )

        # Career recommendations
        recommendations = recommend_careers(
            candidate_skills
        )

        # Learning roadmap
        roadmap = generate_learning_roadmap(
            candidate_skills,
            data.target_role
        )

        # Interview preparation
        interview = prepare_interview(
            candidate_skills,
            data.target_role
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    candidate = parsed["candidate_details"]

    candidate["name"] = (
        candidate["name"] or current_user.full_name
    )

    # Prepare report information
    report_data = {

        "resume_id": resume.id,

        "candidate": candidate,

        "job_title": data.job_title,

        "target_role": data.target_role,

        "education": parsed["education"],

        "technical_skills": candidate_skills,

        "projects": parsed["projects"],

        "experience": parsed["experience"],

        "certifications": parsed["certifications"],

        "matching_results": matching,

        "ats_analysis": ats,

        "career_recommendations": recommendations,

        "learning_roadmap": roadmap,

        "interview": interview

    }

    # Generate unique PDF filename
    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = (
        f"career_report_{current_user.id}_"
        f"{uuid.uuid4().hex}.pdf"
    )

    report_path = REPORT_DIR / filename

    try:

        generate_pdf_report(
            report_data,
            report_path
        )

    except Exception:

        if report_path.exists():
            report_path.unlink()

        raise HTTPException(
            status_code=500,
            detail="PDF report generation failed. Check PowerShell output."
        )

    # Return downloadable PDF
    return FileResponse(
        path=str(report_path.resolve()),
        media_type="application/pdf",
        filename="AI_Career_Intelligence_Report.pdf"
    )
