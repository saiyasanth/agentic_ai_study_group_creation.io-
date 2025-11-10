from faker import Faker
import random
from .database import SessionLocal, init_db
from .crud import create_student, create_course, enroll_student_in_course, add_availability
from .schemas import StudentCreate, CourseCreate, AvailabilityIn

def seed():
    init_db()
    db = SessionLocal()
    try:
        fake = Faker()
        learning_styles = ["visual", "auditory", "kinesthetic", "reading_writing"]
        goal_options = [
            "exam_prep", "project", "skill_exchange", "tutoring", "improve_grades",
            "group_study", "contest_prep"
        ]

        # --- Create 5 sample courses ---
        courses = [
            CourseCreate(code="CS101", name="Intro to CS", difficulty=2, subject="CS"),
            CourseCreate(code="DS200", name="Data Structures", difficulty=4, subject="CS"),
            CourseCreate(code="ML300", name="Machine Learning", difficulty=5, subject="AI"),
            CourseCreate(code="PY110", name="Python Programming", difficulty=2, subject="CS"),
            CourseCreate(code="SE210", name="Software Engg", difficulty=3, subject="CS"),
        ]
        db_courses = [create_course(db, c) for c in courses]

        db_students = []
        for i in range(500):
            name = fake.first_name()
            email = f"{name.lower()}.{i}@example.com"  # Make email unique!
            gpa = round(random.uniform(2.0, 10.0), 2)  # Mixed cgpa between 2.0 and 10.0
            learning_style = random.choice(learning_styles)
            goals = random.sample(goal_options, random.randint(1, 3))
            student = StudentCreate(
                name=name,
                email=email,
                gpa=gpa,
                learning_style=learning_style,
                goals=goals,
            )
            db_student = create_student(db, student)
            db_students.append(db_student)

        # Enroll each student in 1 to 3 random courses
        for student in db_students:
            some_courses = random.sample(db_courses, random.randint(1, 3))
            for course in some_courses:
                enroll_student_in_course(db, student, course)

            # Add availability on 1-2 random weekdays
            for _ in range(random.randint(1, 2)):
                weekday = random.randint(0, 6)
                start_min = random.randint(8, 18) * 60
                end_min = start_min + random.choice([60, 90, 120])
                avail = AvailabilityIn(
                    weekday=weekday,
                    start_min=start_min,
                    end_min=min(end_min, 24 * 60),
                )
                add_availability(db, student, avail)

        print("✅ Seeded DB with 500 students and 5 courses.")

    finally:
        db.close()

if __name__ == "__main__":
    seed()
