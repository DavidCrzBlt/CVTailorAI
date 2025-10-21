from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pathlib import Path
from app.db.database import get_db
from app.db import models
from app.services.langchain_service import llm
from langchain_core.messages import HumanMessage
from app.services.cv_refiner import refine_cv_sections, generate_new_cv, collect_current_sections
from pathlib import Path

router = APIRouter(prefix="/generate", tags=["generator"])
from pathlib import Path

def load_prompt_template(user: models.UserProfile, job: models.JobPosting) -> str:
    template_path = Path(__file__).parent.parent / "templates" / "generate_prompt.txt"
    template_text = template_path.read_text(encoding="utf-8")

    return template_text.format(
        full_name=user.full_name or "",
        headline=user.headline or "",
        skills=user.skills or "",
        tools=user.tools or "",
        experience_md=user.experience_md or "",
        company=job.company or "",
        title=job.title or "",
        raw_description=job.raw_description or ""
    )


@router.get("/{user_id}/{job_id}")
def generate_application(user_id: int, job_id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserProfile).get(user_id)
    job = db.query(models.JobPosting).get(job_id)

    if not user or not job:
        return {"error": "User or Job not found."}

    prompt = load_prompt_template(user, job)
    response = llm.invoke([HumanMessage(content=prompt)])
    markdown_text = response.content
    return {"markdown_output": markdown_text}


@router.get("/refine/{user_id}/{job_id}")
def refine_cv(user_id: int, job_id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserProfile).get(user_id)
    job = db.query(models.JobPosting).get(job_id)
    if not user or not job:
        return {"error": "User or Job not found."}

    template_path = Path(__file__).parent.parent / "templates" / "cv_template.md"
    output_path = Path("generated") / f"cv_refined_{user.id}_{job.id}.md"

    current_sections = collect_current_sections(user, db)
    refined_sections = refine_cv_sections(current_sections, job.raw_description)


    generate_new_cv(template_path, output_path, user, refined_sections)
    return {"message": "Refined CV generated", "path": str(output_path)}