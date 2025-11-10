from sqlalchemy.orm import Session
from . import models


def overlap(a_start, a_end, b_start, b_end):
    """Return overlap duration in minutes."""
    return max(0, min(a_end, b_end) - max(a_start, b_start))


def compatibility(student1: models.Student, student2: models.Student):
    """Simple score based on GPA closeness + availability overlap."""
    score = 0

    # GPA similarity (closer GPA → higher score)
    score += max(0, 10 - abs(student1.gpa - student2.gpa))

    # learning style match
    if student1.learning_style == student2.learning_style:
        score += 2

    # goals overlap
    goals1 = set(student1.goals.split(",")) if student1.goals else set()
    goals2 = set(student2.goals.split(",")) if student2.goals else set()
    score += len(goals1.intersection(goals2)) * 2

    # availability overlap
    for a1 in student1.availability:
        for a2 in student2.availability:
            if a1.weekday == a2.weekday:
                if overlap(a1.start_min, a1.end_min, a2.start_min, a2.end_min) > 0:
                    score += 3

    return score


def top_k_matches(db: Session, student_id: int, k: int = 5):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        return []

    matches = []
    for s in db.query(models.Student).all():
        if s.id == student_id:
            continue
        score = compatibility(student, s)
        matches.append((s.id, score))

    matches.sort(key=lambda x: x[1], reverse=True)
    return matches[:k]
