import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("No se encontró GEMINI_API_KEY en el archivo .env")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=GEMINI_API_KEY,
    temperature=0.3,       
    max_output_tokens=1024
    )

def test_prompt(message: str):
    """
    Envía un prompt simple al modelo Gemini y devuelve la respuesta de texto.
    """
    response = llm.invoke([HumanMessage(content=message)])
    return response.content

def refine_section(section_name: str, section_text: str, job_description: str) -> str:
    template_path = Path(__file__).parent.parent / "templates" / "generate_prompt.txt"
    template_text = template_path.read_text(encoding="utf-8")

    prompt = template_text.format(
        section_name=section_name,
        section_text=section_text,
        job_description=job_description
    )

    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()
