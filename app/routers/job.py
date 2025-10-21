# app/routers/job.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models, schemas

router = APIRouter(prefix="/job", tags=["job"])

@router.post("", response_model=schemas.JobPostingRead)
def create_job_posting(payload: schemas.JobPostingCreate, db: Session = Depends(get_db)):
    job = models.JobPosting(
        company=payload.company,
        title=payload.title,
        source_url=payload.source_url,
        raw_description=payload.raw_description
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("", response_model=list[schemas.JobPostingRead])
def list_job_postings(limit: int = 10, db: Session = Depends(get_db)):
    rows = db.query(models.JobPosting).order_by(models.JobPosting.id.desc()).limit(limit).all()
    return rows

@router.get("/{job_id}", response_model=schemas.JobPostingRead)
def get_job_posting(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.JobPosting).get(job_id)
    return job


