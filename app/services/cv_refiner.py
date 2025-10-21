from app.services.langchain_service import refine_section
from app.utils.sections import CV_SECTIONS
from pathlib import Path
import re, textwrap


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


def collect_current_sections(user) -> dict:
    return {
        "executive_summary": user.headline or "",
        "work_experience": user.experience_md or "",
        "key_skills": user.skills or "",
        "technical_tools": user.tools or "",
        # Si aún no tienes estos campos en BD, déjalos vacíos o fijos:
        "education": "",
        "training": "",
    }
