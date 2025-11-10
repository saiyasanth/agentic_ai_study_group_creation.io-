from typing import List, Optional
from pydantic import BaseModel


class StudentCreate(BaseModel):
    name: str
    email: str
    gpa: float
    learning_style: Optional[str] = None
    goals: List[str]  # will need conversion to CSV in CRUD layer

    class Config:
        orm_mode = True   # ✅ use this for FastAPI + Pydantic v1


class CourseCreate(BaseModel):
    code: str
    name: str
    difficulty: int
    subject: str

    class Config:
        orm_mode = True


class AvailabilityIn(BaseModel):
    weekday: int
    start_min: int
    end_min: int

    class Config:
        orm_mode = True
