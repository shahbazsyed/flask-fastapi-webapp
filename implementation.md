# Student Enrollment System - Implementation Plan

## Project Overview

We'll build a student enrollment system with:
- Student registration
- Course listing
- Enrollment management
- Student dashboard

## Technology Stack

- **API Backend**: FastAPI
- **Web Frontend**: Flask
- **Database**: SQLite (for simplicity)
- **ORM**: SQLAlchemy
- **Templates**: Jinja2
- **HTTP Client**: Requests (for Flask to call FastAPI)

## Implementation Phases

### Phase 1: Project Setup

1. **Directory Structure**
```
student-enrollment-system/
├── fastapi-backend/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic models
│   ├── database.py          # Database configuration
│   └── requirements.txt
├── flask-frontend/
│   ├── app.py               # Flask application
│   ├── templates/           # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── students.html
│   │   ├── courses.html
│   │   └── enrollment.html
│   ├── static/              # CSS, JS files
│   │   └── style.css
│   └── requirements.txt
└── README.md
```

2. **Dependencies**
   - FastAPI: `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`
   - Flask: `flask`, `requests`, `python-dotenv`

### Phase 2: Database Design

1. **Tables Schema**
```sql
Students:
- id (Primary Key)
- student_id (Unique)
- name
- email
- created_at

Courses:
- id (Primary Key)
- course_code (Unique)
- name
- description
- credits
- max_students

Enrollments:
- id (Primary Key)
- student_id (Foreign Key)
- course_id (Foreign Key)
- enrollment_date
- status (enrolled/dropped)
```

2. **SQLAlchemy Models**
```python
# models.py structure
class Student(Base):
    __tablename__ = "students"
    # fields...

class Course(Base):
    __tablename__ = "courses"
    # fields...

class Enrollment(Base):
    __tablename__ = "enrollments"
    # fields...
```

### Phase 3: FastAPI Backend Implementation

1. **Core Setup** (`main.py`)
   - Initialize FastAPI app
   - Configure CORS
   - Set up database connection
   - Create tables on startup

2. **API Endpoints**

   **Student Endpoints:**
   - `GET /students` - List all students
   - `GET /students/{student_id}` - Get student details
   - `POST /students` - Create new student
   - `PUT /students/{student_id}` - Update student
   - `DELETE /students/{student_id}` - Delete student

   **Course Endpoints:**
   - `GET /courses` - List all courses
   - `GET /courses/{course_id}` - Get course details
   - `POST /courses` - Create new course
   - `GET /courses/{course_id}/students` - List enrolled students

   **Enrollment Endpoints:**
   - `POST /enrollments` - Enroll student in course
   - `GET /enrollments/student/{student_id}` - Get student's enrollments
   - `DELETE /enrollments/{enrollment_id}` - Drop course

3. **Pydantic Schemas** (`schemas.py`)
   - Request/Response models
   - Validation rules
   - Type hints

### Phase 4: Flask Frontend Implementation

1. **Core Setup** (`app.py`)
   - Initialize Flask app
   - Configure API base URL
   - Set up template folder
   - Error handling

2. **Routes and Views**

   **Home Page** (`/`)
   - Dashboard with statistics
   - Quick links to main features

   **Student Management** (`/students`)
   - List view with search
   - Add new student form
   - Edit/Delete functionality

   **Course Catalog** (`/courses`)
   - Browse available courses
   - View course details
   - See enrollment count

   **Enrollment** (`/enroll`)
   - Student selection
   - Course selection
   - Enrollment confirmation

3. **Template Structure**

   **Base Template** (`base.html`)
   - Navigation menu
   - Common styling
   - Flash messages

   **Form Templates**
   - Student registration form
   - Course enrollment form
   - Search forms

4. **API Integration**
   ```python
   # Example API call from Flask
   def get_students():
       response = requests.get(f"{API_BASE_URL}/students")
       return response.json()
   ```

### Phase 5: Features Implementation Order

1. **Basic CRUD Operations**
   - Create database models
   - Implement student CRUD in FastAPI
   - Create Flask forms and views
   - Test end-to-end flow

2. **Course Management**
   - Add course endpoints
   - Create course listing page
   - Implement course details view

3. **Enrollment System**
   - Create enrollment API
   - Build enrollment form
   - Add validation (max students, prerequisites)
   - Show enrolled courses on student page

4. **Enhanced Features**
   - Search functionality
   - Sorting and filtering
   - Pagination
   - Export to CSV

### Phase 6: Error Handling and Validation

1. **API Level**
   - Input validation with Pydantic
   - Database constraint handling
   - HTTP status codes
   - Error response format

2. **Frontend Level**
   - Form validation
   - API error display
   - User-friendly messages
   - Loading states

### Phase 7: Testing Strategy

1. **API Testing**
   - Unit tests for endpoints
   - Database transaction tests
   - Validation tests

2. **Integration Testing**
   - Flask-to-FastAPI communication
   - End-to-end user flows
   - Error scenario testing

### Phase 8: Deployment Preparation

1. **Configuration**
   - Environment variables
   - Database connection strings
   - API URLs
   - Secret keys

2. **Running the System**
   ```bash
   # Terminal 1: Start FastAPI
   cd fastapi-backend
   uvicorn main:app --reload --port 8000

   # Terminal 2: Start Flask
   cd flask-frontend
   python app.py
   ```

## Learning Checkpoints

After each phase, students should understand:

1. **Phase 1-2**: Project structure and database design
2. **Phase 3**: How to build RESTful APIs with FastAPI
3. **Phase 4**: How Flask consumes APIs and renders templates
4. **Phase 5**: Feature development workflow
5. **Phase 6**: Proper error handling in distributed systems
6. **Phase 7**: Testing strategies for multi-tier applications
7. **Phase 8**: Deployment considerations

## Common Implementation Patterns

1. **API Client in Flask**
```python
class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get_students(self):
        return requests.get(f"{self.base_url}/students").json()
```

2. **Error Handling**
```python
try:
    response = api_client.create_student(data)
    flash("Student created successfully!", "success")
except requests.exceptions.RequestException:
    flash("Error creating student", "error")
```

3. **Form to API Data**
```python
@app.route("/students/new", methods=["POST"])
def create_student():
    student_data = {
        "name": request.form.get("name"),
        "email": request.form.get("email"),
        "student_id": request.form.get("student_id")
    }
    # Send to API...
```

## Troubleshooting Guide

Common issues students might face:

1. **CORS Errors**: Configure FastAPI CORS middleware
2. **Connection Refused**: Ensure both servers are running
3. **Template Not Found**: Check template file paths
4. **Database Locked**: Use proper session management
5. **JSON Decode Errors**: Validate API responses

## Extensions for Advanced Students

1. Authentication system with JWT
2. File upload for student photos
3. Real-time notifications with WebSockets
4. Admin panel with statistics
5. Email notifications for enrollment
6. Course prerequisites system
7. Grade management
8. Report generation