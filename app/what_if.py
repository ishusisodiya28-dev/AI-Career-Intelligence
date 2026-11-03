
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Resume, User
from app.dependencies import get_current_user

from app.services.resume_parser import parse_resume_text
from app.services.what_if_simulator import simulate_what_if


router = APIRouter(
    prefix="/simulator",
    tags=["What-If Career Simulator"]
)


class WhatIfRequest(BaseModel):

    resume_id: int = Field(gt=0)

    job_role: str = Field(
        min_length=2,
        max_length=150
    )

    additional_skills: list[str] = Field(
        default_factory=list,
        max_length=30
    )


@router.post("/what-if")
def run_what_if_simulation(

    data: WhatIfRequest,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    # Get candidate resume
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

    # Parse candidate skills
    parsed_data = parse_resume_text(
        resume.extracted_text
    )

    candidate_skills = parsed_data["technical_skills"]

    # Run hypothetical simulation
    try:

        result = simulate_what_if(
            candidate_skills,
            data.job_role,
            data.additional_skills
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

        "message": "What-If Simulation completed!",

        "candidate_name": candidate_name,

        "resume_id": resume.id,

        "candidate_current_skills": candidate_skills,

        "simulation_results": result

    }
