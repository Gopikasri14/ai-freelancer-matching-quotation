import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db import get_db
from ...models import Project, Freelancer, Quotation
from ...schemas import QuotationRequest, QuotationOut
from ...services.quotation import predict

router = APIRouter()

@router.post("/generate", response_model=QuotationOut)
def generate(payload: QuotationRequest, db: Session = Depends(get_db)):
    project = db.get(Project, payload.project_id)
    freelancer = db.get(Freelancer, payload.freelancer_id)
    if not project or not freelancer:
        raise HTTPException(404, "Project or freelancer not found")
    try:
        result = predict(project, freelancer)
    except RuntimeError as exc:
        raise HTTPException(503, str(exc))
    q = Quotation(project_id=project.id, freelancer_id=freelancer.id, **{
        k: v for k, v in result.items() if k in {
            "predicted_effort", "effort_min", "effort_max", "base_price",
            "final_min_price", "final_max_price", "included_revisions", "extra_revision_price"
        }
    }, adjustments=json.dumps(result["adjustments"]))
    db.add(q)
    db.commit()
    db.refresh(q)
    return {**result, "id": q.id, "project_id": project.id, "freelancer_id": freelancer.id}
