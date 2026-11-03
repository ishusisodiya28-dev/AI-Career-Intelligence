
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Resume, User
from app.dependencies import get_current_user

from app.services.resume_parser import parse_resume_text
from app.services.learning_roadmap import generate_learning_roadmap


router = APIRouter(
    prefix="/roadmap",
    tags=["Personalized Learning Roadmap"]
)


class RoadmapRequest(BaseModel):

    resume_id: int = Field(gt=0)

    job_role: str = Field(
        min_length=2,
        max_length=150
    )


@router.post("/generate")
def generate_roadmap(

    data: RoadmapRequest,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    resume = db.query(Resume).filter(
        Resume.id == data.resume_id,
        Resume.user_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Resume not found"
        )

    parsed_data = parse_resume_text(
        resume.extracted_text or ""
    )

    candidate_skills = parsed_data["technical_skills"]

    try:

        roadmap = generate_learning_roadmap(
            candidate_skills,
            data.job_role
        )

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    candidate_name = (
        parsed_data["candidate_details"]["name"]
        or current_user.full_name
    )

    return {

        "message": "Personalized learning roadmap generated successfully!",

        "candidate_name": candidate_name,

        "resume_id": resume.id,

        "candidate_skills": candidate_skills,

        "learning_roadmap": roadmap

    }
