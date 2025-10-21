# app/db/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    headline = Column(String(200), nullable=True)           # “Executive summary” corto
    skills = Column(Text, nullable=True)                    # CSV o JSON (por ahora texto)
    tools = Column(Text, nullable=True)                     # idem
    experience_md = Column(Text, nullable=True)             # “bloques” en Markdown
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class JobPosting(Base):
    __tablename__ = "job_postings"
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(120), nullable=True)
    title = Column(String(180), nullable=True)
    source_url = Column(String(500), nullable=True)
    raw_description = Column(Text, nullable=False)          # texto pegado o parseado
    created_at = Column(DateTime, server_default=func.now())
