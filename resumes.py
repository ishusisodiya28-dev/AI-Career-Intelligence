
import os
import uuid

from pathlib import Path
from io import BytesIO

import pymupdf
from docx import Document

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Resume, User
from app.dependencies import get_current_user

from app.services.resume_parser import parse_resume_text


router = APIRouter(
    prefix="/resume",
    tags=["Resume Management"]
)

UPLOAD_DIR = Path("uploads")

MAX_FILE_SIZE = 10 * 1024 * 1024


# PDF text extraction
def extract_pdf_text(content: bytes):

    with pymupdf.open(
        stream=content,
        filetype="pdf"
    ) as pdf:

        text = "\n".join(
            page.get_text()
            for page in pdf
        )

    return text.strip()


# DOCX text extraction
def extract_docx_text(content: bytes):

    document = Document(
        BytesIO(content)
    )

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
    ]

    table_text = []

    for table in document.tables:

        for row in table.rows:

            for cell in row.cells:
                table_text.append(cell.text)

    return "\n".join(
        paragraphs + table_text
    ).strip()


# Resume Upload API
@router.post("/upload")
async def upload_resume(

    file: UploadFile = File(...),

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Please select a resume file"
        )

    original_filename = os.path.basename(
        file.filename.replace("\\", "/")
    )

    extension = Path(
        original_filename
    ).suffix.lower()

    if extension not in [".pdf", ".docx"]:

        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed"
        )

    content = await file.read(
        MAX_FILE_SIZE + 1
    )

    if not content:

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    if len(content) > MAX_FILE_SIZE:

        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 10 MB"
        )

    try:

        if extension == ".pdf":

            if not content.startswith(b"%PDF-"):
                raise ValueError("Invalid PDF")

            extracted_text = extract_pdf_text(
                content
            )

        else:

            if not content.startswith(b"PK"):
                raise ValueError("Invalid DOCX")

            extracted_text = extract_docx_text(
                content
            )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid or unreadable resume file"
        )

    if not extracted_text:

        raise HTTPException(
            status_code=422,
            detail="No readable text found in resume"
        )

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    stored_filename = (
        f"{uuid.uuid4().hex}{extension}"
    )

    file_path = UPLOAD_DIR / stored_filename

    try:

        file_path.write_bytes(content)

        new_resume = Resume(

            user_id=current_user.id,

            original_filename=original_filename,

            stored_filename=stored_filename,

            file_path=str(file_path),

            extracted_text=extracted_text

        )

        db.add(new_resume)

        db.commit()

        db.refresh(new_resume)

    except Exception:

        db.rollback()

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail="Resume could not be saved"
        )

    return {

        "message": "Resume uploaded successfully!",

        "resume_id": new_resume.id,

        "filename": original_filename,

        "extracted_text_length": len(extracted_text),

        "text_preview": extracted_text[:500]

    }


# Get Current User Resumes
@router.get("/my-resumes")
def get_my_resumes(

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    resumes = db.query(Resume).filter(

        Resume.user_id == current_user.id

    ).all()

    return {

        "total_resumes": len(resumes),

        "resumes": [

            {

                "id": resume.id,

                "filename": resume.original_filename,

                "uploaded_at": resume.uploaded_at

            }

            for resume in resumes

        ]

    }


# AI Resume Parsing API
@router.get("/{resume_id}/parse")
def parse_my_resume(

    resume_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)

):

    resume = db.query(Resume).filter(

        Resume.id == resume_id,

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

    return {

        "message": "Resume parsed successfully!",

        "resume_id": resume.id,

        "filename": resume.original_filename,

        "parsed_data": parsed_data

    }
