from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from .database import get_db
from . import models, scoring

router = APIRouter()


# ✅ Request body schema
class RecommendationRequest(BaseModel):
    student_id: int
    top_k: int = 5


@router.post("/recommendations")
def recommend(request: RecommendationRequest, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == request.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    matches = scoring.top_k_matches(db, request.student_id, request.top_k)

    result: List[dict] = []
    for sid, score in matches:
        s = db.query(models.Student).filter(models.Student.id == sid).first()
        if s:
            result.append(
                {
                    "id": s.id,
                    "name": s.name,
                    "email": s.email,
                    "gpa": s.gpa,
                    "learning_style": s.learning_style,
                    # 🔄 Convert CSV to list for frontend
                    "goals": s.goals.split(",") if s.goals else [],
                    "score": score,
                }
            )

    return {"student_id": request.student_id, "matches": result}
