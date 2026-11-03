
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Resume, User
from app.dependencies import get_current_user

from app.services.job_matcher import calculate_job_match
from app.services.resume_parser import parse_resume_text
from app.services.ats_checker import evaluate_ats
from app.services.career_recommender import recommend_careers


router = APIRouter(
    prefix="/analysis",
    tags=["AI Job Analysis"]
)


class JobMatchRequest(BaseModel):
    resume_id: int = Field(gt=0)
    job_title: str = Field(min_length=2, max_length=150)
    job_description: str = Field(
        min_length=30,
        max_length=15000
    )


class ResumeRequest(BaseModel):
    resume_id: int = Field(gt=0)


def get_user_resume(resume_id, db, current_user):

    resume = db.query(Resume).filter(
        Resume.id == resume_id,
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

    return resume


# API 1: Job Matching
@router.post("/match")
def analyze_job_match(
    data: JobMatchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    resume = get_user_resume(
        data.resume_id, db, current_user
    )

    result = calculate_job_match(
        resume.extracted_text,
        data.job_description
    )

    parsed_data = parse_resume_text(
        resume.extracted_text
    )

    candidate_name = (
        parsed_data["candidate_details"]["name"]
        or current_user.full_name
    )

    return {
        "message": "AI Job Analysis completed!",
        "candidate_name": candidate_name,
        "job_title": data.job_title,
        "resume_id": resume.id,
        "matching_results": result,
        "score_method": (
            "60% skill match + 40% TF-IDF text similarity"
        ),
        "note": (
            "Partially matched skills are not "
            "automatically inferred."
        )
    }


# API 2: ATS Compatibility and Skill Gap
@router.post("/ats-check")
def ats_compatibility_check(
    data: JobMatchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    resume = get_user_resume(
        data.resume_id, db, current_user
    )

    ats_result = evaluate_ats(
        resume.extracted_text,
        data.job_description
    )

    match_result = calculate_job_match(
        resume.extracted_text,
        data.job_description
    )

    parsed_data = parse_resume_text(
        resume.extracted_text
    )

    candidate_name = (
        parsed_data["candidate_details"]["name"]
        or current_user.full_name
    )

    return {
        "message": "ATS Analysis completed!",
        "candidate_name": candidate_name,
        "job_title": data.job_title,
        "resume_id": resume.id,
        "ats_analysis": ats_result,
        "skill_gap_analysis": {
            "available_skills": match_result["available_skills"],
            "required_skills": match_result["required_skills"],
            "matched_skills": match_result["matched_skills"],
            "missing_skills": match_result["missing_skills"],
            "partially_matched_skills": []
        }
    }


# API 3: Career Recommendations
@router.post("/career-recommendations")
def career_recommendation(
    data: ResumeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    resume = get_user_resume(
        data.resume_id, db, current_user
    )

    parsed_data = parse_resume_text(
        resume.extracted_text
    )

    candidate_skills = (
        parsed_data["technical_skills"]
    )

    recommendations = recommend_careers(
        candidate_skills
    )

    candidate_name = (
        parsed_data["candidate_details"]["name"]
        or current_user.full_name
    )

    return {
        "message": "Career recommendations generated successfully!",
        "candidate_name": candidate_name,
        "resume_id": resume.id,
        "candidate_skills": candidate_skills,
        "total_recommendations": len(recommendations),
        "recommendations": recommendations,
        "note": (
            "Recommendations are based on overlap "
            "with predefined role skills. Match scores "
            "are not hiring probabilities."
        )
    }
