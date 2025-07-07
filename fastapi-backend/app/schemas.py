"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional, List


# Student Schemas
class StudentBase(BaseModel):
    """Base schema for Student"""
    student_id: str = Field(..., min_length=1, max_length=50, description="Unique student ID")
    name: str = Field(..., min_length=1, max_length=100, description="Student full name")
    email: EmailStr = Field(..., description="Student email address")


class StudentCreate(StudentBase):
    """Schema for creating a new student"""
    pass


class StudentUpdate(BaseModel):
    """Schema for updating a student"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None


class StudentRead(StudentBase):
    """Schema for reading student data"""
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class StudentWithEnrollments(StudentRead):
    """Schema for student with their enrollments"""
    enrollments: List["EnrollmentWithCourse"] = []


# Course Schemas
class CourseBase(BaseModel):
    """Base schema for Course"""
    course_code: str = Field(..., min_length=1, max_length=20, description="Unique course code")
    name: str = Field(..., min_length=1, max_length=100, description="Course name")
    description: Optional[str] = Field(None, description="Course description")
    credits: int = Field(..., ge=1, le=12, description="Number of credits")
    max_students: int = Field(30, ge=1, le=500, description="Maximum number of students")


class CourseCreate(CourseBase):
    """Schema for creating a new course"""
    pass


class CourseUpdate(BaseModel):
    """Schema for updating a course"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    credits: Optional[int] = Field(None, ge=1, le=12)
    max_students: Optional[int] = Field(None, ge=1, le=500)


class CourseRead(CourseBase):
    """Schema for reading course data"""
    id: int
    enrolled_count: int = Field(default=0, description="Number of enrolled students")
    available_seats: int = Field(default=30, description="Number of available seats")
    
    model_config = ConfigDict(from_attributes=True)


class CourseWithStudents(CourseRead):
    """Schema for course with enrolled students"""
    enrollments: List["EnrollmentWithStudent"] = []


# Enrollment Schemas
class EnrollmentBase(BaseModel):
    """Base schema for Enrollment"""
    student_id: int = Field(..., description="Student ID")
    course_id: int = Field(..., description="Course ID")


class EnrollmentCreate(EnrollmentBase):
    """Schema for creating a new enrollment"""
    pass


class EnrollmentRead(EnrollmentBase):
    """Schema for reading enrollment data"""
    id: int
    enrollment_date: datetime
    status: str = Field(..., description="Enrollment status (active, dropped, completed)")
    
    model_config = ConfigDict(from_attributes=True)


class EnrollmentWithStudent(EnrollmentRead):
    """Schema for enrollment with student details"""
    student: StudentRead


class EnrollmentWithCourse(EnrollmentRead):
    """Schema for enrollment with course details"""
    course: CourseRead


class EnrollmentUpdate(BaseModel):
    """Schema for updating enrollment status"""
    status: str = Field(..., pattern="^(active|dropped|completed)$", description="New enrollment status")


# Response Schemas
class SuccessResponse(BaseModel):
    """Generic success response"""
    message: str
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    """Generic error response"""
    error: str
    detail: Optional[str] = None


# Pagination Response Schema
from typing import TypeVar, Generic

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    """Generic pagination response"""
    items: List[T]
    total: int
    page: int
    per_page: int
    
    model_config = ConfigDict(from_attributes=True)


# Update forward references
StudentWithEnrollments.model_rebuild()
CourseWithStudents.model_rebuild()