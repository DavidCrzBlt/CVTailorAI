import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# --- Verificación de URL ---
if not DATABASE_URL:
    print("FATAL ERROR: No se encontró la variable de entorno DATABASE_URL.")
    # Usar sys.exit(1) detiene la aplicación si la clave esencial falta.
    sys.exit(1)
# ---------------------------

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
