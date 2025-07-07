#!/usr/bin/env python3
"""
Quick test script to verify the API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:", response.json())

def test_create_students():
    """Test creating students"""
    students = [
        {
            "student_id": "S001",
            "name": "John Doe",
            "email": "john.doe@example.com"
        },
        {
            "student_id": "S002",
            "name": "Jane Smith",
            "email": "jane.smith@example.com"
        },
        {
            "student_id": "S003",
            "name": "Bob Johnson",
            "email": "bob.johnson@example.com"
        }
    ]
    
    for student in students:
        response = requests.post(f"{BASE_URL}/students", json=student)
        if response.status_code == 201:
            print(f"Created student: {student['name']}")
        else:
            print(f"Error creating student: {response.text}")

def test_create_courses():
    """Test creating courses"""
    courses = [
        {
            "course_code": "CS101",
            "name": "Introduction to Computer Science",
            "description": "Basic concepts of programming and computer science",
            "credits": 3,
            "max_students": 50
        },
        {
            "course_code": "MATH201",
            "name": "Calculus I",
            "description": "Differential and integral calculus",
            "credits": 4,
            "max_students": 30
        },
        {
            "course_code": "ENG101",
            "name": "English Composition",
            "description": "Academic writing and critical thinking",
            "credits": 3,
            "max_students": 25
        }
    ]
    
    for course in courses:
        response = requests.post(f"{BASE_URL}/courses", json=course)
        if response.status_code == 201:
            print(f"Created course: {course['name']}")
        else:
            print(f"Error creating course: {response.text}")

def test_list_students():
    """Test listing students"""
    response = requests.get(f"{BASE_URL}/students")
    print("\nStudents:", json.dumps(response.json(), indent=2))

def test_list_courses():
    """Test listing courses"""
    response = requests.get(f"{BASE_URL}/courses")
    print("\nCourses:", json.dumps(response.json(), indent=2))

def test_enroll_students():
    """Test enrolling students in courses"""
    # First get student and course IDs
    students = requests.get(f"{BASE_URL}/students").json()
    courses = requests.get(f"{BASE_URL}/courses").json()
    
    if students and courses:
        # Enroll first student in first two courses
        enrollments = [
            {"student_id": students[0]["id"], "course_id": courses[0]["id"]},
            {"student_id": students[0]["id"], "course_id": courses[1]["id"]},
            {"student_id": students[1]["id"], "course_id": courses[0]["id"]},
            {"student_id": students[2]["id"], "course_id": courses[2]["id"]},
        ]
        
        for enrollment in enrollments:
            response = requests.post(f"{BASE_URL}/enrollments", json=enrollment)
            if response.status_code == 201:
                print(f"Enrolled student {enrollment['student_id']} in course {enrollment['course_id']}")
            else:
                print(f"Error enrolling: {response.text}")

def test_get_student_enrollments():
    """Test getting student enrollments"""
    students = requests.get(f"{BASE_URL}/students").json()
    if students:
        student_id = students[0]["id"]
        response = requests.get(f"{BASE_URL}/enrollments/student/{student_id}")
        print(f"\nEnrollments for student {student_id}:", json.dumps(response.json(), indent=2))

def test_stats():
    """Test statistics endpoint"""
    response = requests.get(f"{BASE_URL}/stats")
    print("\nSystem Statistics:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    print("Testing FastAPI endpoints...")
    print("=" * 50)
    
    try:
        test_health()
        print("\nCreating test data...")
        test_create_students()
        test_create_courses()
        test_enroll_students()
        
        print("\nFetching data...")
        test_list_students()
        test_list_courses()
        test_get_student_enrollments()
        test_stats()
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Make sure the FastAPI server is running on port 8000.")
    except Exception as e:
        print(f"Error: {e}")