"""
Example usage of the database models
"""
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Student, Course, Enrollment
from .init_db import init_db


def create_sample_data():
    """Create some sample data for testing"""
    db = SessionLocal()
    try:
        # Create sample students
        student1 = Student(
            student_id="S001",
            name="John Doe",
            email="john.doe@example.com"
        )
        student2 = Student(
            student_id="S002",
            name="Jane Smith",
            email="jane.smith@example.com"
        )
        
        # Create sample courses
        course1 = Course(
            course_code="CS101",
            name="Introduction to Computer Science",
            description="Basic concepts of computer science and programming",
            credits=3,
            max_students=50
        )
        course2 = Course(
            course_code="MATH201",
            name="Calculus I",
            description="Differential calculus and its applications",
            credits=4,
            max_students=30
        )
        
        # Add to database
        db.add_all([student1, student2, course1, course2])
        db.commit()
        
        # Create enrollments
        enrollment1 = Enrollment(
            student_id=student1.id,
            course_id=course1.id,
            status="active"
        )
        enrollment2 = Enrollment(
            student_id=student2.id,
            course_id=course1.id,
            status="active"
        )
        enrollment3 = Enrollment(
            student_id=student1.id,
            course_id=course2.id,
            status="active"
        )
        
        db.add_all([enrollment1, enrollment2, enrollment3])
        db.commit()
        
        print("Sample data created successfully!")
        
        # Query and display data
        print("\nStudents:")
        students = db.query(Student).all()
        for student in students:
            print(f"  - {student.name} ({student.student_id}) - {student.email}")
            
        print("\nCourses:")
        courses = db.query(Course).all()
        for course in courses:
            print(f"  - {course.name} ({course.course_code}) - {course.credits} credits")
            print(f"    Enrolled: {course.enrolled_count}/{course.max_students}")
            
        print("\nEnrollments:")
        enrollments = db.query(Enrollment).all()
        for enrollment in enrollments:
            print(f"  - {enrollment.student.name} enrolled in {enrollment.course.name}")
            
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


def test_relationships():
    """Test the relationships between models"""
    db = SessionLocal()
    try:
        # Get a student with their enrollments
        student = db.query(Student).filter_by(student_id="S001").first()
        if student:
            print(f"\nEnrollments for {student.name}:")
            for enrollment in student.enrollments:
                print(f"  - {enrollment.course.name} (Status: {enrollment.status})")
        
        # Get a course with its students
        course = db.query(Course).filter_by(course_code="CS101").first()
        if course:
            print(f"\nStudents enrolled in {course.name}:")
            for enrollment in course.enrollments:
                if enrollment.status == "active":
                    print(f"  - {enrollment.student.name}")
                    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    # Initialize database
    print("Initializing database...")
    init_db()
    
    # Create sample data
    create_sample_data()
    
    # Test relationships
    test_relationships()