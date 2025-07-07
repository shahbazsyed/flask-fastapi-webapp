"""
Main FastAPI application for student enrollment system
"""
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
import logging

from app.database import engine, get_db
from app import models, schemas

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI instance
app = FastAPI(
    title="Student Enrollment API",
    description="RESTful API for managing students, courses, and enrollments",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://localhost:5001"],  # Flask frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "student-enrollment-api"}


# ======================== STUDENT ENDPOINTS ========================

@app.get("/students", response_model=schemas.PaginatedResponse[schemas.StudentRead])
def list_students(
    skip: int = Query(0, ge=0, description="Number of students to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of students to return"),
    search: Optional[str] = Query(None, description="Search by name or email"),
    db: Session = Depends(get_db)
):
    """
    List all students with optional pagination and search
    """
    query = db.query(models.Student)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (models.Student.name.ilike(search_term)) |
            (models.Student.email.ilike(search_term)) |
            (models.Student.student_id.ilike(search_term))
        )
    
    # Get total count before pagination
    total = query.count()
    
    # Get paginated results
    students = query.offset(skip).limit(limit).all()
    
    # Calculate current page
    page = (skip // limit) + 1 if limit > 0 else 1
    
    return {
        "items": students,
        "total": total,
        "page": page,
        "per_page": limit
    }


@app.post("/students", response_model=schemas.StudentRead, status_code=201)
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new student
    """
    # Check if student_id or email already exists
    existing_student = db.query(models.Student).filter(
        (models.Student.student_id == student.student_id) |
        (models.Student.email == student.email)
    ).first()
    
    if existing_student:
        if existing_student.student_id == student.student_id:
            raise HTTPException(status_code=400, detail="Student ID already exists")
        else:
            raise HTTPException(status_code=400, detail="Email already exists")
    
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    
    try:
        db.commit()
        db.refresh(db_student)
        logger.info(f"Created new student: {db_student.student_id}")
        return db_student
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error creating student: {e}")
        raise HTTPException(status_code=400, detail="Error creating student")


@app.get("/students/{student_id}", response_model=schemas.StudentWithEnrollments)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a student by ID with their enrollments
    """
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.put("/students/{student_id}", response_model=schemas.StudentRead)
def update_student(
    student_id: int,
    student_update: schemas.StudentUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a student's information
    """
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    update_data = student_update.model_dump(exclude_unset=True)
    
    # Check if email is being updated and if it already exists
    if "email" in update_data:
        existing_student = db.query(models.Student).filter(
            models.Student.email == update_data["email"],
            models.Student.id != student_id
        ).first()
        if existing_student:
            raise HTTPException(status_code=400, detail="Email already exists")
    
    for field, value in update_data.items():
        setattr(student, field, value)
    
    try:
        db.commit()
        db.refresh(student)
        logger.info(f"Updated student: {student.student_id}")
        return student
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error updating student: {e}")
        raise HTTPException(status_code=400, detail="Error updating student")


@app.delete("/students/{student_id}", status_code=204)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a student
    """
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(student)
    db.commit()
    logger.info(f"Deleted student: {student.student_id}")
    return None


# ======================== COURSE ENDPOINTS ========================

@app.get("/courses", response_model=schemas.PaginatedResponse[schemas.CourseRead])
def list_courses(
    skip: int = Query(0, ge=0, description="Number of courses to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of courses to return"),
    search: Optional[str] = Query(None, description="Search by name, code, or description"),
    available_only: bool = Query(False, description="Show only courses with available seats"),
    db: Session = Depends(get_db)
):
    """
    List all courses with optional pagination, search, and filtering
    """
    query = db.query(models.Course)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (models.Course.name.ilike(search_term)) |
            (models.Course.course_code.ilike(search_term)) |
            (models.Course.description.ilike(search_term))
        )
    
    # Get total count before pagination
    total = query.count()
    
    # Get paginated results
    courses = query.offset(skip).limit(limit).all()
    
    # Filter available courses in Python (since it's a computed property)
    if available_only:
        # When filtering by available_only, we need to adjust the total count
        all_courses = query.all()
        available_courses = [course for course in all_courses if course.available_seats > 0]
        total = len(available_courses)
        # Re-paginate the filtered results
        courses = available_courses[skip:skip + limit]
    
    # Calculate current page
    page = (skip // limit) + 1 if limit > 0 else 1
    
    return {
        "items": courses,
        "total": total,
        "page": page,
        "per_page": limit
    }


@app.post("/courses", response_model=schemas.CourseRead, status_code=201)
def create_course(
    course: schemas.CourseCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new course
    """
    # Check if course_code already exists
    existing_course = db.query(models.Course).filter(
        models.Course.course_code == course.course_code
    ).first()
    
    if existing_course:
        raise HTTPException(status_code=400, detail="Course code already exists")
    
    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    
    try:
        db.commit()
        db.refresh(db_course)
        logger.info(f"Created new course: {db_course.course_code}")
        return db_course
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error creating course: {e}")
        raise HTTPException(status_code=400, detail="Error creating course")


@app.get("/courses/{course_id}", response_model=schemas.CourseRead)
def get_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a course by ID
    """
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.get("/courses/{course_id}/students", response_model=schemas.CourseWithStudents)
def get_course_students(
    course_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all students enrolled in a course
    """
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Filter only active enrollments
    course.enrollments = [e for e in course.enrollments if e.status == "active"]
    return course


@app.put("/courses/{course_id}", response_model=schemas.CourseRead)
def update_course(
    course_id: int,
    course_update: schemas.CourseUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a course's information
    """
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    update_data = course_update.model_dump(exclude_unset=True)
    
    # Check if reducing max_students below current enrollment
    if "max_students" in update_data:
        if update_data["max_students"] < course.enrolled_count:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot set max_students to {update_data['max_students']} when {course.enrolled_count} students are enrolled"
            )
    
    for field, value in update_data.items():
        setattr(course, field, value)
    
    try:
        db.commit()
        db.refresh(course)
        logger.info(f"Updated course: {course.course_code}")
        return course
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error updating course: {e}")
        raise HTTPException(status_code=400, detail="Error updating course")


@app.delete("/courses/{course_id}", status_code=204)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a course (will cascade delete enrollments)
    """
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if there are active enrollments
    active_enrollments = [e for e in course.enrollments if e.status == "active"]
    if active_enrollments:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete course with {len(active_enrollments)} active enrollments"
        )
    
    db.delete(course)
    db.commit()
    logger.info(f"Deleted course: {course.course_code}")
    return None


# ======================== ENROLLMENT ENDPOINTS ========================

@app.post("/enrollments", response_model=schemas.EnrollmentRead, status_code=201)
def create_enrollment(
    enrollment: schemas.EnrollmentCreate,
    db: Session = Depends(get_db)
):
    """
    Enroll a student in a course
    """
    # Check if student exists
    student = db.query(models.Student).filter(
        models.Student.id == enrollment.student_id
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check if course exists
    course = db.query(models.Course).filter(
        models.Course.id == enrollment.course_id
    ).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check if course has available seats
    if course.available_seats <= 0:
        raise HTTPException(status_code=400, detail="Course is full")
    
    # Check if student is already enrolled
    existing_enrollment = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == enrollment.student_id,
        models.Enrollment.course_id == enrollment.course_id
    ).first()
    
    if existing_enrollment:
        if existing_enrollment.status == "active":
            raise HTTPException(status_code=400, detail="Student is already enrolled in this course")
        else:
            # Reactivate the enrollment
            existing_enrollment.status = "active"
            db.commit()
            db.refresh(existing_enrollment)
            logger.info(f"Reactivated enrollment: Student {student.student_id} in Course {course.course_code}")
            return existing_enrollment
    
    # Create new enrollment
    db_enrollment = models.Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        status="active"
    )
    db.add(db_enrollment)
    
    try:
        db.commit()
        db.refresh(db_enrollment)
        logger.info(f"Created enrollment: Student {student.student_id} in Course {course.course_code}")
        return db_enrollment
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error creating enrollment: {e}")
        raise HTTPException(status_code=400, detail="Error creating enrollment")


@app.get("/enrollments", response_model=schemas.PaginatedResponse[schemas.EnrollmentRead])
def list_enrollments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None, regex="^(active|dropped|completed)$"),
    db: Session = Depends(get_db)
):
    """
    List all enrollments with optional filtering
    """
    query = db.query(models.Enrollment)
    
    if status:
        query = query.filter(models.Enrollment.status == status)
    
    # Get total count before pagination
    total = query.count()
    
    # Get paginated results
    enrollments = query.offset(skip).limit(limit).all()
    
    # Calculate current page
    page = (skip // limit) + 1 if limit > 0 else 1
    
    return {
        "items": enrollments,
        "total": total,
        "page": page,
        "per_page": limit
    }


@app.get("/enrollments/student/{student_id}", response_model=schemas.PaginatedResponse[schemas.EnrollmentWithCourse])
def get_student_enrollments(
    student_id: int,
    status: Optional[str] = Query(None, regex="^(active|dropped|completed)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get all enrollments for a specific student
    """
    # Check if student exists
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    query = db.query(models.Enrollment).filter(
        models.Enrollment.student_id == student_id
    )
    
    if status:
        query = query.filter(models.Enrollment.status == status)
    
    # Get total count before pagination
    total = query.count()
    
    # Get paginated results
    enrollments = query.offset(skip).limit(limit).all()
    
    # Calculate current page
    page = (skip // limit) + 1 if limit > 0 else 1
    
    return {
        "items": enrollments,
        "total": total,
        "page": page,
        "per_page": limit
    }


@app.get("/enrollments/course/{course_id}", response_model=schemas.PaginatedResponse[schemas.EnrollmentWithStudent])
def get_course_enrollments(
    course_id: int,
    status: Optional[str] = Query(None, regex="^(active|dropped|completed)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get all enrollments for a specific course
    """
    # Check if course exists
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    query = db.query(models.Enrollment).filter(
        models.Enrollment.course_id == course_id
    )
    
    if status:
        query = query.filter(models.Enrollment.status == status)
    
    # Get total count before pagination
    total = query.count()
    
    # Get paginated results
    enrollments = query.offset(skip).limit(limit).all()
    
    # Calculate current page
    page = (skip // limit) + 1 if limit > 0 else 1
    
    return {
        "items": enrollments,
        "total": total,
        "page": page,
        "per_page": limit
    }


@app.put("/enrollments/{enrollment_id}", response_model=schemas.EnrollmentRead)
def update_enrollment(
    enrollment_id: int,
    enrollment_update: schemas.EnrollmentUpdate,
    db: Session = Depends(get_db)
):
    """
    Update enrollment status (e.g., drop a course)
    """
    enrollment = db.query(models.Enrollment).filter(
        models.Enrollment.id == enrollment_id
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    # Update status
    enrollment.status = enrollment_update.status
    
    try:
        db.commit()
        db.refresh(enrollment)
        logger.info(f"Updated enrollment {enrollment_id} status to {enrollment.status}")
        return enrollment
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating enrollment: {e}")
        raise HTTPException(status_code=400, detail="Error updating enrollment")


@app.delete("/enrollments/{enrollment_id}", status_code=204)
def delete_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete an enrollment record completely
    """
    enrollment = db.query(models.Enrollment).filter(
        models.Enrollment.id == enrollment_id
    ).first()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    db.delete(enrollment)
    db.commit()
    logger.info(f"Deleted enrollment {enrollment_id}")
    return None


# ======================== UTILITY ENDPOINTS ========================

@app.get("/stats")
def get_statistics(db: Session = Depends(get_db)):
    """
    Get system statistics
    """
    total_students = db.query(models.Student).count()
    total_courses = db.query(models.Course).count()
    active_enrollments = db.query(models.Enrollment).filter(
        models.Enrollment.status == "active"
    ).count()
    
    return {
        "total_students": total_students,
        "total_courses": total_courses,
        "total_enrollments": active_enrollments,
        "active_enrollments": active_enrollments
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)