from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...db import get_db
from ...models import Project
from ...schemas import ProjectCreate, ProjectOut

router = APIRouter()

@router.post("", response_model=ProjectOut)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.get("", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).order_by(Project.id.desc()).all()
