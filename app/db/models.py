# app/db/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    headline = Column(String(200), nullable=True)
    skills = Column(Text, nullable=True)
    tools = Column(Text, nullable=True)
    experience_md = Column(Text, nullable=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relaciones nuevas
    skill_set = relationship("Skill", back_populates="user", cascade="all, delete")
    experience_set = relationship("Experience", back_populates="user", cascade="all, delete")
    education_set = relationship("Education", back_populates="user", cascade="all, delete")

# --- SKILLS ---
class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id", ondelete="CASCADE"))
    name = Column(String(100), nullable=False)
    category = Column(String(100), nullable=True)
    level = Column(Integer, nullable=True)

    user = relationship("UserProfile", back_populates="skill_set")


# --- EXPERIENCE ---
class Experience(Base):
    __tablename__ = "experiences"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id", ondelete="CASCADE"))
    company = Column(String(120), nullable=False)
    position = Column(String(120), nullable=True)
    start_date = Column(String(50), nullable=True)
    end_date = Column(String(50), nullable=True)
    achievements = Column(Text, nullable=True)

    user = relationship("UserProfile", back_populates="experience_set")


# --- EDUCATION ---
class Education(Base):
    __tablename__ = "education"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id", ondelete="CASCADE"))
    institution = Column(String(200), nullable=False)
    degree = Column(String(200), nullable=False)
    start_year = Column(String(10), nullable=True)
    end_year = Column(String(10), nullable=True)
    description = Column(Text, nullable=True)

    user = relationship("UserProfile", back_populates="education_set")


class JobPosting(Base):
    __tablename__ = "job_postings"
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(120), nullable=True)
    title = Column(String(180), nullable=True)
    source_url = Column(String(500), nullable=True)
    raw_description = Column(Text, nullable=False)          # texto pegado o parseado
    created_at = Column(DateTime, server_default=func.now())
