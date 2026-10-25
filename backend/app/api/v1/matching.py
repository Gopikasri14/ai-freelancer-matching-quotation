from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db import get_db
from ...models import Project, Freelancer, Match
from ...ml.matcher import match_freelancers
from ...schemas import MatchOut

router = APIRouter()

@router.post("/projects/{project_id}", response_model=list[MatchOut])
def recommend(project_id: int, db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(404, "Project not found")
    freelancers = db.query(Freelancer).filter(Freelancer.availability == "Available").all()
    ranked = match_freelancers(project, freelancers, top_k=5)
    db.query(Match).filter(Match.project_id == project_id).delete()
    result = []
    for rank, (f, score) in enumerate(ranked, start=1):
        db.add(Match(project_id=project_id, freelancer_id=f.id, similarity_score=score, rank=rank))
        result.append({
            "id": f.id, "name": f.name, "bio": f.bio,
            "skills": [s.strip() for s in f.skills.split(",") if s.strip()],
            "experience_years": f.experience_years, "hourly_rate": f.hourly_rate,
            "minimum_rate": f.minimum_rate, "availability": f.availability,
            "similarity_score": round(score, 4), "rank": rank
        })
    db.commit()
    return result
