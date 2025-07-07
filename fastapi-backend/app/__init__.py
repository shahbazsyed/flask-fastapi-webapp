"""
FastAPI Backend Package for Student Enrollment System
"""
from .database import Base, engine, get_db
from .models import Student, Course, Enrollment
from .schemas import (
    StudentCreate, StudentRead, StudentUpdate, StudentWithEnrollments,
    CourseCreate, CourseRead, CourseUpdate, CourseWithStudents,
    EnrollmentCreate, EnrollmentRead, EnrollmentUpdate,
    EnrollmentWithStudent, EnrollmentWithCourse,
    SuccessResponse, ErrorResponse
)

__all__ = [
    # Database
    "Base", "engine", "get_db",
    
    # Models
    "Student", "Course", "Enrollment",
    
    # Schemas
    "StudentCreate", "StudentRead", "StudentUpdate", "StudentWithEnrollments",
    "CourseCreate", "CourseRead", "CourseUpdate", "CourseWithStudents",
    "EnrollmentCreate", "EnrollmentRead", "EnrollmentUpdate",
    "EnrollmentWithStudent", "EnrollmentWithCourse",
    "SuccessResponse", "ErrorResponse"
]