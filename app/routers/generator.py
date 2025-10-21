from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pathlib import Path
from app.db.database import get_db
from app.db import models
from app.services.langchain_service import llm
from langchain_core.messages import HumanMessage
from app.services.cv_refiner import refine_cv_sections, generate_new_cv, collect_current_sections
from pathlib import Path


from app.services.pdf_service import markdown_to_pdf
import re

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



@router.post("/save/{user_id}/{job_id}")
def save_application(user_id: int, job_id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserProfile).get(user_id)
    job = db.query(models.JobPosting).get(job_id)
    if not user or not job:
        return {"error": "User or Job not found."}

    # Leer CV refinado
    md_path = Path("generated") / f"cv_refined_{user.id}_{job.id}.md"
    if not md_path.exists():
        return {"error": "No refined CV found for this user/job"}

    cv_text = md_path.read_text(encoding="utf-8")

    # Separar por secciones (## Cover Letter y ## Email si existen)
    def extract_section(title, text):
        pattern = rf"## {title}\n(.*?)(?=\n##|\Z)"
        match = re.search(pattern, text, re.S)
        return match.group(1).strip() if match else ""

    cv_md = extract_section("Executive Summary", cv_text) + "\n\n" + extract_section("Work Experience", cv_text)
    cover_md = extract_section("Cover Letter", cv_text)
    email_md = extract_section("Email", cv_text)

    # Crear registro
    app_entry = models.Application(
        user_id=user_id,
        job_id=job_id,
        cv_md=cv_md,
        cover_letter_md=cover_md,
        email_md=email_md
    )
    db.add(app_entry)
    db.commit()
    db.refresh(app_entry)

    # Generar PDF opcionalmente
    pdf_path = markdown_to_pdf(cv_text, f"cv_{user.id}_{job.id}")

    return {
        "message": "Application saved successfully",
        "application_id": app_entry.id,
        "pdf": str(pdf_path)
    }
