#!/usr/bin/env python3
"""Initialize the database with sample data for testing."""

import requests
import random
from datetime import datetime, timedelta

API_BASE_URL = "http://localhost:8000"

# Sample student data
STUDENTS = [
    {"student_id": "STU001", "name": "Alice Johnson", "email": "alice.johnson@university.edu"},
    {"student_id": "STU002", "name": "Bob Smith", "email": "bob.smith@university.edu"},
    {"student_id": "STU003", "name": "Carol Davis", "email": "carol.davis@university.edu"},
    {"student_id": "STU004", "name": "David Wilson", "email": "david.wilson@university.edu"},
    {"student_id": "STU005", "name": "Emma Brown", "email": "emma.brown@university.edu"},
    {"student_id": "STU006", "name": "Frank Miller", "email": "frank.miller@university.edu"},
    {"student_id": "STU007", "name": "Grace Lee", "email": "grace.lee@university.edu"},
    {"student_id": "STU008", "name": "Henry Chen", "email": "henry.chen@university.edu"},
]

# Sample course data
COURSES = [
    {
        "course_code": "CS101",
        "name": "Introduction to Computer Science",
        "description": "Fundamentals of programming and computational thinking",
        "credits": 3,
        "max_students": 30
    },
    {
        "course_code": "CS201",
        "name": "Data Structures and Algorithms",
        "description": "Advanced programming concepts and algorithm design",
        "credits": 4,
        "max_students": 25
    },
    {
        "course_code": "MATH101",
        "name": "Calculus I",
        "description": "Differential and integral calculus",
        "credits": 4,
        "max_students": 40
    },
    {
        "course_code": "PHYS101",
        "name": "Physics I",
        "description": "Mechanics and thermodynamics",
        "credits": 4,
        "max_students": 35
    },
    {
        "course_code": "ENG101",
        "name": "English Composition",
        "description": "Academic writing and critical thinking",
        "credits": 3,
        "max_students": 20
    },
    {
        "course_code": "HIST101",
        "name": "World History",
        "description": "Global historical perspectives from ancient to modern times",
        "credits": 3,
        "max_students": 45
    },
    {
        "course_code": "BIO101",
        "name": "Introduction to Biology",
        "description": "Fundamentals of life sciences",
        "credits": 4,
        "max_students": 30
    },
    {
        "course_code": "CHEM101",
        "name": "General Chemistry",
        "description": "Basic principles of chemistry",
        "credits": 4,
        "max_students": 25
    }
]

def check_api_health():
    """Check if the API is running."""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

def create_students():
    """Create sample students."""
    print("\nCreating students...")
    created_students = []
    
    for student in STUDENTS:
        try:
            response = requests.post(f"{API_BASE_URL}/students", json=student)
            if response.status_code == 201:
                created_student = response.json()
                created_students.append(created_student)
                print(f"✓ Created student: {student['name']}")
            elif response.status_code == 409:
                print(f"⚠ Student already exists: {student['name']}")
                # Get the existing student
                students_response = requests.get(f"{API_BASE_URL}/students")
                if students_response.status_code == 200:
                    for s in students_response.json()["items"]:
                        if s["student_id"] == student["student_id"]:
                            created_students.append(s)
                            break
            else:
                print(f"✗ Failed to create student: {student['name']} - {response.text}")
        except Exception as e:
            print(f"✗ Error creating student {student['name']}: {e}")
    
    return created_students

def create_courses():
    """Create sample courses."""
    print("\nCreating courses...")
    created_courses = []
    
    for course in COURSES:
        try:
            response = requests.post(f"{API_BASE_URL}/courses", json=course)
            if response.status_code == 201:
                created_course = response.json()
                created_courses.append(created_course)
                print(f"✓ Created course: {course['name']}")
            elif response.status_code == 409:
                print(f"⚠ Course already exists: {course['name']}")
                # Get the existing course
                courses_response = requests.get(f"{API_BASE_URL}/courses")
                if courses_response.status_code == 200:
                    for c in courses_response.json()["items"]:
                        if c["course_code"] == course["course_code"]:
                            created_courses.append(c)
                            break
            else:
                print(f"✗ Failed to create course: {course['name']} - {response.text}")
        except Exception as e:
            print(f"✗ Error creating course {course['name']}: {e}")
    
    return created_courses

def create_enrollments(students, courses):
    """Create random enrollments."""
    print("\nCreating enrollments...")
    
    # Each student enrolls in 2-5 courses
    for student in students:
        num_courses = random.randint(2, 5)
        selected_courses = random.sample(courses, min(num_courses, len(courses)))
        
        for course in selected_courses:
            enrollment_data = {
                "student_id": student["id"],
                "course_id": course["id"]
            }
            
            try:
                response = requests.post(f"{API_BASE_URL}/enrollments", json=enrollment_data)
                if response.status_code == 201:
                    print(f"✓ Enrolled {student['name']} in {course['name']}")
                elif response.status_code == 409:
                    print(f"⚠ {student['name']} already enrolled in {course['name']}")
                else:
                    print(f"✗ Failed to enroll {student['name']} in {course['name']}: {response.text}")
            except Exception as e:
                print(f"✗ Error enrolling {student['name']} in {course['name']}: {e}")

def main():
    """Initialize the database with sample data."""
    print("Student Enrollment System - Sample Data Initialization")
    print("=" * 50)
    
    # Check if API is running
    print("Checking API health...")
    if not check_api_health():
        print("✗ Error: FastAPI backend is not running!")
        print("Please start the backend server first with: ./run_backend.sh")
        return
    
    print("✓ API is healthy")
    
    # Create sample data
    students = create_students()
    courses = create_courses()
    
    if students and courses:
        create_enrollments(students, courses)
    
    # Show statistics
    print("\n" + "=" * 50)
    print("Sample data initialization complete!")
    
    try:
        stats_response = requests.get(f"{API_BASE_URL}/stats")
        if stats_response.status_code == 200:
            stats = stats_response.json()
            print(f"\nDatabase Statistics:")
            print(f"- Total Students: {stats['total_students']}")
            print(f"- Total Courses: {stats['total_courses']}")
            print(f"- Total Enrollments: {stats['total_enrollments']}")
    except:
        pass
    
    print("\nYou can now access the application at http://localhost:5001")

if __name__ == "__main__":
    main()