# Database Models Documentation

## Overview
This document describes the database models and schemas used in the Student Enrollment System's FastAPI backend.

## Database Configuration

### Files Structure
- `database.py` - SQLAlchemy database setup and session management
- `models.py` - SQLAlchemy ORM models (Student, Course, Enrollment)
- `schemas.py` - Pydantic models for request/response validation
- `config.py` - Application configuration settings
- `init_db.py` - Database initialization script

## Models

### Student Model
Represents a student in the system.

**Table**: `students`

**Columns**:
- `id` (Integer, Primary Key) - Auto-incrementing ID
- `student_id` (String[50], Unique, Required) - Student's unique identifier
- `name` (String[100], Required) - Student's full name
- `email` (String[100], Unique, Required) - Student's email address
- `created_at` (DateTime) - Timestamp of record creation

**Relationships**:
- `enrollments` - One-to-many relationship with Enrollment model

### Course Model
Represents a course available for enrollment.

**Table**: `courses`

**Columns**:
- `id` (Integer, Primary Key) - Auto-incrementing ID
- `course_code` (String[20], Unique, Required) - Course code (e.g., "CS101")
- `name` (String[100], Required) - Course name
- `description` (Text, Optional) - Course description
- `credits` (Integer, Required) - Number of credits
- `max_students` (Integer, Required, Default: 30) - Maximum enrollment capacity

**Relationships**:
- `enrollments` - One-to-many relationship with Enrollment model

**Properties**:
- `enrolled_count` - Calculated property returning number of active enrollments
- `available_seats` - Calculated property returning remaining seats

### Enrollment Model
Junction table representing student-course enrollments.

**Table**: `enrollments`

**Columns**:
- `id` (Integer, Primary Key) - Auto-incrementing ID
- `student_id` (Integer, Foreign Key) - References students.id
- `course_id` (Integer, Foreign Key) - References courses.id
- `enrollment_date` (DateTime) - Timestamp of enrollment
- `status` (String[20], Required, Default: "active") - Enrollment status

**Status Values**:
- `active` - Currently enrolled
- `dropped` - Student dropped the course
- `completed` - Course completed

**Relationships**:
- `student` - Many-to-one relationship with Student model
- `course` - Many-to-one relationship with Course model

**Constraints**:
- Unique constraint on (student_id, course_id) - prevents duplicate enrollments

## Pydantic Schemas

### Request Schemas
- `StudentCreate` - Create new student
- `StudentUpdate` - Update existing student
- `CourseCreate` - Create new course
- `CourseUpdate` - Update existing course
- `EnrollmentCreate` - Create new enrollment
- `EnrollmentUpdate` - Update enrollment status

### Response Schemas
- `StudentRead` - Return student data
- `StudentWithEnrollments` - Student with enrolled courses
- `CourseRead` - Return course data
- `CourseWithStudents` - Course with enrolled students
- `EnrollmentRead` - Return enrollment data
- `EnrollmentWithStudent` - Enrollment with student details
- `EnrollmentWithCourse` - Enrollment with course details

### Utility Schemas
- `SuccessResponse` - Generic success response
- `ErrorResponse` - Generic error response

## Usage Examples

### Initialize Database
```python
from app.init_db import init_db
init_db()  # Creates all tables
```

### Create a Student
```python
from app.database import SessionLocal
from app.models import Student

db = SessionLocal()
student = Student(
    student_id="S12345",
    name="John Doe",
    email="john@example.com"
)
db.add(student)
db.commit()
```

### Query with Relationships
```python
# Get student with enrollments
student = db.query(Student).filter_by(student_id="S12345").first()
for enrollment in student.enrollments:
    print(f"Enrolled in: {enrollment.course.name}")

# Get course with students
course = db.query(Course).filter_by(course_code="CS101").first()
active_students = [e.student for e in course.enrollments if e.status == "active"]
```

## Database Migrations
For production use, consider using Alembic for database migrations instead of `init_db.py`.