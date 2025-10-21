from fastapi import FastAPI
from app.db.database import engine, Base
from app.routers import user, job, generator
from app.services.langchain_service import test_prompt


app = FastAPI(title="CVTailorAI", version="0.1.0")

# Crea tablas si no existen (MVP; más adelante usamos Alembic)
Base.metadata.create_all(bind=engine)

app.include_router(user.router)
app.include_router(job.router)
app.include_router(generator.router)


@app.get("/")
def root():
    return {"ok": True, "service": "CVTailorAI"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/test-gemini")
def test_gemini(prompt: str = "Dime una frase motivadora corta"):
    response = test_prompt(prompt)
    return {"response": response}

