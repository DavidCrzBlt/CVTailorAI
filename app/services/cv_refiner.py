from app.services.langchain_service import refine_section
from app.utils.sections import CV_SECTIONS
from pathlib import Path
import re, textwrap
from typing import Dict
from app.db import models

def refine_cv_sections(current_sections: dict, job_description: str) -> dict:
    refined = {}
    for section in CV_SECTIONS:
        source_text = current_sections.get(section, "")
        if not source_text.strip():
            refined[section] = ""  # no hay nada que refinar
            continue
        refined[section] = refine_section(section, source_text, job_description)
    return refined



def fill_template(template_text: str, replacements: dict) -> str:
    """
    Sustituye los placeholders {key} por su valor en replacements.
    Si una clave no está en replacements, la deja vacía.
    """
    result = template_text
    for key, value in replacements.items():
        result = result.replace(f"{{{key}}}", textwrap.dedent(value).strip())
    return result


def generate_new_cv(cv_template_path: Path, output_path: Path, user, refined_sections: dict):
    template = cv_template_path.read_text(encoding="utf-8")
    replacements = {
        "name": user.full_name,
        "location": "Toluca, Mexico",
        "telephone": "+52 722 744 4949",
        "email": "david.crzbel@gmail.com",
        "linkedin": "https://www.linkedin.com/in/david-cruz-beltran/",
        **refined_sections,
    }
    filled = fill_template(template, replacements)
    output_path.write_text(filled, encoding="utf-8")
    return output_path


def collect_current_sections(user: models.UserProfile, db) -> Dict[str, str]:
    """
    Combina información del usuario con sus tablas relacionadas
    (skills, experiences, education, etc.)
    y la devuelve lista para pasar al LLM.
    """
    # --- Executive Summary (headline) ---
    executive_summary = user.headline or ""

    # --- Work Experience ---
    experiences = db.query(models.Experience).filter_by(user_id=user.id).all()
    exp_text = ""
    for exp in experiences:
        exp_text += f"### {exp.company} — {exp.position or ''}\n"
        if exp.start_date or exp.end_date:
            exp_text += f"({exp.start_date or ''} - {exp.end_date or ''})\n"
        exp_text += f"{exp.achievements or ''}\n\n"

    # --- Key Skills ---
    skills = db.query(models.Skill).filter_by(user_id=user.id).all()
    skill_lines = [f"- {s.name} ({s.category or ''}, Level {s.level or 'N/A'})" for s in skills]
    skills_text = "\n".join(skill_lines)

    # --- Technical Tools (puede ser subset de skills si quieres filtrarlo después) ---
    tools = [s.name for s in skills if s.category and s.category.lower() in ("tools", "framework", "platform")]
    tools_text = ", ".join(tools) if tools else user.tools or ""

    # --- Education ---
    education = db.query(models.Education).filter_by(user_id=user.id).all()
    edu_text = ""
    for e in education:
        edu_text += f"**{e.degree}**, {e.institution} ({e.start_year or ''}-{e.end_year or ''})\n"
        if e.description:
            edu_text += f"{e.description}\n\n"

    # --- Training (por ahora vacío o rellenable manualmente) ---
    training_text = user.skills or ""

    return {
        "executive_summary": executive_summary,
        "work_experience": exp_text.strip(),
        "key_skills": skills_text.strip(),
        "technical_tools": tools_text.strip(),
        "education": edu_text.strip(),
        "training": training_text.strip()
    }
