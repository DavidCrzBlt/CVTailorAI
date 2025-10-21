from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db import models, schemas

router = APIRouter(prefix="/user", tags=["user"])

# app/routers/user.py (debajo del esqueleto)
@router.post("", response_model=schemas.UserProfileRead)
def create_user_profile(payload: schemas.UserProfileCreate, db: Session = Depends(get_db)):
    profile = models.UserProfile(
        full_name=payload.full_name,
        headline=payload.headline,
        skills=payload.skills,
        tools=payload.tools,
        experience_md=payload.experience_md,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/{user_id}", response_model=schemas.UserProfileRead)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(models.UserProfile).get(user_id)
    if not profile:
        # FastAPI convertirá esto en 404 si retornas None con response_model, pero
        # es mejor lanzar una excepción (lo haremos luego). Por ahora devolvemos None.
        return None
    return profile

@router.get("", response_model=list[schemas.UserProfileRead])
def list_user_profiles(limit: int = 10, db: Session = Depends(get_db)):
    rows = db.query(models.UserProfile).order_by(models.UserProfile.id.desc()).limit(limit).all()
    return rows

