from pydantic import BaseModel, Field
from typing import Optional

class ProjectCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=10)
    project_type: str
    complexity: str
    expected_hours: Optional[float] = Field(default=None, gt=0)
    deadline_days: int = Field(gt=0, le=365)
    revisions: int = Field(default=2, ge=0, le=20)
    budget: Optional[float] = Field(default=None, gt=0)

class ProjectOut(ProjectCreate):
    id: int
    class Config:
        from_attributes = True

class FreelancerOut(BaseModel):
    id: int
    name: str
    bio: str
    skills: list[str]
    experience_years: int
    hourly_rate: float
    minimum_rate: float
    availability: str

class MatchOut(FreelancerOut):
    similarity_score: float
    rank: int

class QuotationRequest(BaseModel):
    project_id: int
    freelancer_id: int

class QuotationOut(BaseModel):
    id: int
    project_id: int
    freelancer_id: int
    predicted_effort: float
    effort_min: float
    effort_max: float
    base_price: float
    final_min_price: float
    final_max_price: float
    included_revisions: int
    extra_revision_price: float
    adjustments: dict
