from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Many-to-Many: Students <-> Courses
student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id")),
    Column("course_id", Integer, ForeignKey("courses.id")),
)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    gpa = Column(Float, nullable=False)
    learning_style = Column(String, nullable=True)
    goals = Column(String, nullable=True)  # store as CSV

    courses = relationship("Course", secondary=student_course, back_populates="students")
    availability = relationship("Availability", back_populates="student")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    difficulty = Column(Integer, nullable=False)
    subject = Column(String, nullable=True)

    students = relationship("Student", secondary=student_course, back_populates="courses")


class Availability(Base):
    __tablename__ = "availability"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    weekday = Column(Integer, nullable=False)  # 0=Mon, 6=Sun
    start_min = Column(Integer, nullable=False)  # minutes from midnight
    end_min = Column(Integer, nullable=False)

    student = relationship("Student", back_populates="availability")
