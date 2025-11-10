from sqlalchemy.orm import Session
from . import models, schemas

def create_student(db: Session, student: schemas.StudentCreate):
    # Check for duplicate email before inserting (returns existing if found)
    existing = db.query(models.Student).filter(models.Student.email == student.email).first()
    if existing:
        return existing
    db_student = models.Student(
        name=student.name,
        email=student.email,
        gpa=student.gpa,
        learning_style=student.learning_style,
        goals=",".join(student.goals),
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def create_course(db: Session, course: schemas.CourseCreate):
    # Check for duplicate course code before inserting
    existing = db.query(models.Course).filter(models.Course.code == course.code).first()
    if existing:
        return existing
    db_course = models.Course(
        code=course.code,
        name=course.name,
        difficulty=course.difficulty,
        subject=course.subject,
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def enroll_student_in_course(db: Session, student: models.Student, course: models.Course):
    # Avoid duplicate enrollments
    if course not in student.courses:
        student.courses.append(course)
        db.commit()

def add_availability(db: Session, student: models.Student, avail: schemas.AvailabilityIn):
    # Check for duplicate availability (optional, usually fine to allow overlaps)
    db_avail = models.Availability(
        student_id=student.id,
        weekday=avail.weekday,
        start_min=avail.start_min,
        end_min=avail.end_min,
    )
    db.add(db_avail)
    db.commit()
    db.refresh(db_avail)
    return db_avail
