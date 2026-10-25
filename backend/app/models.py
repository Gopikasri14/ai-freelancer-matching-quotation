from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class Freelancer(Base):
    __tablename__ = "freelancers"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    bio = Column(Text, default="")
    skills = Column(Text, default="")
    experience_years = Column(Integer, default=0)
    hourly_rate = Column(Float, default=500.0)
    minimum_rate = Column(Float, default=500.0)
    availability = Column(String(50), default="Available")
    matches = relationship("Match", back_populates="freelancer")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    project_type = Column(String(80), nullable=False)
    complexity = Column(String(30), nullable=False)
    expected_hours = Column(Float, nullable=True)
    deadline_days = Column(Integer, nullable=False)
    revisions = Column(Integer, default=2)
    budget = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    matches = relationship("Match", back_populates="project")
    quotations = relationship("Quotation", back_populates="project")

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    freelancer_id = Column(Integer, ForeignKey("freelancers.id"), nullable=False)
    similarity_score = Column(Float, nullable=False)
    rank = Column(Integer, nullable=False)
    project = relationship("Project", back_populates="matches")
    freelancer = relationship("Freelancer", back_populates="matches")

class Quotation(Base):
    __tablename__ = "quotations"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    freelancer_id = Column(Integer, ForeignKey("freelancers.id"), nullable=False)
    predicted_effort = Column(Float, nullable=False)
    base_price = Column(Float, nullable=False)
    effort_min = Column(Float, nullable=False)
    effort_max = Column(Float, nullable=False)
    final_min_price = Column(Float, nullable=False)
    final_max_price = Column(Float, nullable=False)
    included_revisions = Column(Integer, nullable=False)
    extra_revision_price = Column(Float, nullable=False)
    adjustments = Column(Text, default="{}")
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="quotations")
