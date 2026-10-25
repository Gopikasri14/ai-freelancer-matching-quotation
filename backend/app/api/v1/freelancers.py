from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...db import get_db
from ...models import Freelancer
from ...schemas import FreelancerOut

router = APIRouter()

@router.get("", response_model=list[FreelancerOut])
def list_freelancers(db: Session = Depends(get_db)):
    rows = db.query(Freelancer).all()
    return [to_out(x) for x in rows]

def to_out(x):
    return {
        "id": x.id, "name": x.name, "bio": x.bio,
        "skills": [s.strip() for s in x.skills.split(",") if s.strip()],
        "experience_years": x.experience_years,
        "hourly_rate": x.hourly_rate,
        "minimum_rate": x.minimum_rate,
        "availability": x.availability
    }
