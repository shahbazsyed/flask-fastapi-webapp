# System Architecture Diagrams

## 1. High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Student Enrollment System                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐         ┌──────────────┐         ┌──────────────┐      │
│  │   Browser    │ <-----> │ Flask Server │ <-----> │FastAPI Server│      │
│  │  (Client)    │  HTML   │  (Port 5000) │  JSON   │ (Port 8000) │      │
│  └──────────────┘         └──────────────┘         └──────────────┘      │
│         ↑                         ↑                         ↑             │
│         │                         │                         │             │
│         │                    ┌────────────┐                │             │
│         │                    │   Static   │                │             │
│         └────────────────────│   Files    │                │             │
│                             │ CSS/JS/IMG  │                │             │
│                             └────────────┘                 │             │
│                                                           │             │
│                                                    ┌──────────────┐    │
│                                                    │   SQLite     │    │
│                                                    │   Database   │    │
│                                                    └──────────────┘    │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

## 2. Request Flow Architecture

```
┌─────────┐      ┌─────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
│ Browser │      │  Flask  │      │ FastAPI  │      │SQLAlchemy│      │ Database │
└────┬────┘      └────┬────┘      └────┬─────┘      └────┬─────┘      └────┬─────┘
     │                │                 │                  │                  │
     │ GET /students  │                 │                  │                  │
     │───────────────>│                 │                  │                  │
     │                │                 │                  │                  │
     │                │ GET /students   │                  │                  │
     │                │────────────────>│                  │                  │
     │                │                 │                  │                  │
     │                │                 │ Query Students   │                  │
     │                │                 │─────────────────>│                  │
     │                │                 │                  │                  │
     │                │                 │                  │ SELECT * FROM    │
     │                │                 │                  │ students        │
     │                │                 │                  │────────────────>│
     │                │                 │                  │                  │
     │                │                 │                  │ ResultSet       │
     │                │                 │                  │<────────────────│
     │                │                 │                  │                  │
     │                │                 │ Student Objects  │                  │
     │                │                 │<─────────────────│                  │
     │                │                 │                  │                  │
     │                │ JSON Response   │                  │                  │
     │                │<────────────────│                  │                  │
     │                │                 │                  │                  │
     │                │ Render Template │                  │                  │
     │                │ with Data       │                  │                  │
     │                │                 │                  │                  │
     │ HTML Response  │                 │                  │                  │
     │<───────────────│                 │                  │                  │
     │                │                 │                  │                  │
```

## 3. Component Architecture

### Flask Frontend Component
```
┌─────────────────────────────────────────────────────────┐
│                    Flask Frontend                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │   Routes    │  │  Templates   │  │  API Client   │ │
│  ├─────────────┤  ├──────────────┤  ├───────────────┤ │
│  │ /           │  │ base.html    │  │ get_students()│ │
│  │ /students   │  │ index.html   │  │ get_courses() │ │
│  │ /courses    │  │ students.html│  │ create_student│ │
│  │ /enroll     │  │ courses.html │  │ enroll()      │ │
│  └─────────────┘  └──────────────┘  └───────────────┘ │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │   Forms     │  │   Static     │  │    Utils      │ │
│  ├─────────────┤  ├──────────────┤  ├───────────────┤ │
│  │ StudentForm │  │ style.css    │  │ error_handler │ │
│  │ CourseForm  │  │ script.js    │  │ flash_message │ │
│  │ EnrollForm  │  │ images/      │  │ validators    │ │
│  └─────────────┘  └──────────────┘  └───────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### FastAPI Backend Component
```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Backend                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │  Endpoints  │  │   Models     │  │   Schemas     │ │
│  ├─────────────┤  ├──────────────┤  ├───────────────┤ │
│  │ /students   │  │ Student      │  │ StudentCreate │ │
│  │ /courses    │  │ Course       │  │ StudentRead   │ │
│  │ /enrollments│  │ Enrollment   │  │ CourseCreate  │ │
│  │ /health     │  │              │  │ CourseRead    │ │
│  └─────────────┘  └──────────────┘  └───────────────┘ │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐ │
│  │  Database   │  │ Middleware   │  │  Depends      │ │
│  ├─────────────┤  ├──────────────┤  ├───────────────┤ │
│  │ engine      │  │ CORS         │  │ get_db()      │ │
│  │ SessionLocal│  │ Logging      │  │ auth_check()  │ │
│  │ Base        │  │ Error Handler│  │ validate()    │ │
│  └─────────────┘  └──────────────┘  └───────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 4. Database Schema Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Database Schema                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────┐         ┌─────────────────────┐          │
│  │      STUDENTS       │         │      COURSES        │          │
│  ├─────────────────────┤         ├─────────────────────┤          │
│  │ id (PK)            │         │ id (PK)            │          │
│  │ student_id (UNIQUE)│         │ course_code (UNIQUE)│          │
│  │ name               │         │ name               │          │
│  │ email              │         │ description        │          │
│  │ created_at         │         │ credits            │          │
│  └──────────┬──────────┘         │ max_students       │          │
│             │                    └──────────┬──────────┘          │
│             │                                │                      │
│             │    ┌─────────────────────┐    │                      │
│             │    │    ENROLLMENTS      │    │                      │
│             │    ├─────────────────────┤    │                      │
│             │    │ id (PK)            │    │                      │
│             └────┤ student_id (FK)    ├────┘                      │
│                  │ course_id (FK)     │                           │
│                  │ enrollment_date    │                           │
│                  │ status             │                           │
│                  └─────────────────────┘                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## 5. API Endpoint Architecture

```
FastAPI Endpoints Structure
│
├── /students
│   ├── GET    /students           → List all students
│   ├── POST   /students           → Create new student
│   ├── GET    /students/{id}      → Get student details
│   ├── PUT    /students/{id}      → Update student
│   └── DELETE /students/{id}      → Delete student
│
├── /courses
│   ├── GET    /courses            → List all courses
│   ├── POST   /courses            → Create new course
│   ├── GET    /courses/{id}       → Get course details
│   └── GET    /courses/{id}/students → Get enrolled students
│
└── /enrollments
    ├── POST   /enrollments        → Enroll student
    ├── GET    /enrollments/student/{id} → Get student enrollments
    └── DELETE /enrollments/{id}   → Drop enrollment
```

## 6. Form Submission Flow

```
┌──────────┐     ┌───────────┐     ┌──────────┐     ┌─────────┐     ┌──────────┐
│  User    │     │   Flask   │     │ FastAPI  │     │   ORM   │     │    DB    │
│  Form    │     │   Route   │     │ Endpoint │     │         │     │          │
└────┬─────┘     └─────┬─────┘     └────┬─────┘     └────┬────┘     └────┬─────┘
     │                 │                 │                │               │
     │ Submit Form     │                 │                │               │
     │────────────────>│                 │                │               │
     │                 │                 │                │               │
     │                 │ Validate Data   │                │               │
     │                 │                 │                │               │
     │                 │ POST /students  │                │               │
     │                 │────────────────>│                │               │
     │                 │                 │                │               │
     │                 │                 │ Validate Schema│               │
     │                 │                 │                │               │
     │                 │                 │ Create Object  │               │
     │                 │                 │───────────────>│               │
     │                 │                 │                │               │
     │                 │                 │                │ INSERT INTO   │
     │                 │                 │                │──────────────>│
     │                 │                 │                │               │
     │                 │                 │                │ Success       │
     │                 │                 │                │<──────────────│
     │                 │                 │                │               │
     │                 │                 │ Student Object │               │
     │                 │                 │<───────────────│               │
     │                 │                 │                │               │
     │                 │ 201 Created     │                │               │
     │                 │<────────────────│                │               │
     │                 │                 │                │               │
     │ Success Page    │                 │                │               │
     │<────────────────│                 │                │               │
     │                 │                 │                │               │
```

## 7. Error Handling Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Error Handling Flow                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Client Request                                                │
│        │                                                        │
│        ▼                                                        │
│   Flask Route ──────> Try/Catch Block                         │
│        │                    │                                   │
│        │                    ▼                                   │
│        │              API Request                              │
│        │                    │                                   │
│        │         ┌──────────┴──────────┐                      │
│        │         │                     │                       │
│        │    Success               API Error                    │
│        │         │                     │                       │
│        │         │                     ▼                       │
│        │         │              Error Handler                  │
│        │         │                     │                       │
│        │         │            ┌────────┴────────┐             │
│        │         │            │                 │             │
│        │         │      4XX Error         5XX Error           │
│        │         │            │                 │             │
│        │         │            ▼                 ▼             │
│        │         │      User Message     System Error         │
│        │         │            │                 │             │
│        │         └────────────┴─────────────────┘             │
│        │                            │                          │
│        │                            ▼                          │
│        └─────────────────> Render Response                    │
│                                    │                           │
│                                    ▼                           │
│                            Return to Client                    │
│                                                                │
└─────────────────────────────────────────────────────────────────┘
```

## 8. Session and State Management

```
┌─────────────────────────────────────────────────────────────────┐
│                  Session Management Architecture                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Browser                    Flask                    FastAPI    │
│  ┌──────────┐         ┌───────────────┐       ┌─────────────┐ │
│  │ Cookies  │ <-----> │ Session Store │       │  Stateless  │ │
│  │          │         │               │       │             │ │
│  │ SESSID=  │         │ User Data     │       │ No Sessions │ │
│  │ abc123   │         │ Flash Messages│       │             │ │
│  └──────────┘         │ Form Data     │       │ JWT Tokens  │ │
│                       └───────────────┘       │ (if auth)   │ │
│                                               └─────────────┘ │
│                                                                │
└─────────────────────────────────────────────────────────────────┘
```

## 9. Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Production Deployment                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐                                               │
│  │   Nginx     │  Port 80/443                                  │
│  │  (Reverse   │                                               │
│  │   Proxy)    │                                               │
│  └──────┬──────┘                                               │
│         │                                                       │
│    ┌────┴────┐                                                 │
│    │         │                                                 │
│    ▼         ▼                                                 │
│ ┌──────────────┐         ┌──────────────┐                     │
│ │   Gunicorn   │         │   Uvicorn    │                     │
│ │               │         │               │                     │
│ │ Flask Workers│         │FastAPI Workers│                     │
│ │  Port 5000   │         │  Port 8000   │                     │
│ └───────┬──────┘         └───────┬──────┘                     │
│         │                         │                             │
│         └─────────────┬───────────┘                            │
│                       │                                         │
│                 ┌─────▼─────┐                                  │
│                 │PostgreSQL │                                  │
│                 │    or     │                                  │
│                 │  MySQL    │                                  │
│                 └───────────┘                                  │
│                                                                │
└─────────────────────────────────────────────────────────────────┘
```

## 10. User Flows - When Flask and FastAPI Are Used

### Flow 1: Viewing Student List
```
User Action: Navigates to /students
│
├─> FLASK handles the request
│   ├─> Checks user session/authentication
│   ├─> Calls FastAPI: GET http://localhost:8000/students
│   └─> Waits for response
│
├─> FASTAPI processes the request
│   ├─> Connects to database via SQLAlchemy
│   ├─> Executes query: SELECT * FROM students
│   ├─> Serializes data to JSON using Pydantic
│   └─> Returns JSON response
│
└─> FLASK receives JSON response
    ├─> Parses JSON data
    ├─> Passes data to Jinja2 template
    ├─> Renders students.html with data
    └─> Returns HTML to browser
```

### Flow 2: Creating New Student
```
User Action: Fills and submits student registration form
│
├─> FLASK handles POST to /students/new
│   ├─> Validates form data (client-side validation)
│   ├─> Prepares JSON payload from form data
│   ├─> Calls FastAPI: POST http://localhost:8000/students
│   └─> Includes JSON body with student data
│
├─> FASTAPI processes the request
│   ├─> Validates data with Pydantic schema
│   ├─> Creates Student model instance
│   ├─> Saves to database via SQLAlchemy
│   ├─> Returns success response with created student
│   └─> Or returns validation errors
│
└─> FLASK handles the response
    ├─> If success:
    │   ├─> Sets flash message "Student created successfully"
    │   └─> Redirects to student list
    └─> If error:
        ├─> Sets error flash message
        └─> Re-renders form with errors
```

### Flow 3: Course Enrollment
```
User Action: Selects student and course, clicks "Enroll"
│
├─> FLASK handles POST to /enroll
│   ├─> Validates student_id and course_id
│   ├─> Checks if user has permission
│   ├─> Calls FastAPI: POST http://localhost:8000/enrollments
│   └─> Sends enrollment data
│
├─> FASTAPI processes enrollment
│   ├─> Validates student exists
│   ├─> Validates course exists
│   ├─> Checks enrollment constraints:
│   │   ├─> Course not full
│   │   ├─> Student not already enrolled
│   │   └─> Prerequisites met (if any)
│   ├─> Creates enrollment record
│   └─> Returns success or error
│
└─> FLASK handles the response
    ├─> Updates session data if needed
    ├─> Shows appropriate message
    └─> Redirects to appropriate page
```

### Flow 4: Searching for Courses
```
User Action: Types in search box and submits
│
├─> FLASK handles GET to /courses?search=math
│   ├─> Extracts search parameter
│   ├─> Calls FastAPI: GET http://localhost:8000/courses?search=math
│   └─> May add user-specific filters
│
├─> FASTAPI processes search
│   ├─> Builds SQL query with LIKE clause
│   ├─> Executes search on course name/description
│   ├─> Returns filtered results
│   └─> Includes pagination info
│
└─> FLASK renders results
    ├─> Displays matching courses
    ├─> Shows "No results" if empty
    └─> Maintains search term in input
```

### Flow 5: Student Dashboard
```
User Action: Clicks on student name to view details
│
├─> FLASK handles GET to /students/{id}
│   ├─> Extracts student ID from URL
│   ├─> Makes parallel API calls:
│   │   ├─> GET http://localhost:8000/students/{id}
│   │   └─> GET http://localhost:8000/enrollments/student/{id}
│   └─> Waits for both responses
│
├─> FASTAPI processes both requests
│   ├─> Request 1: Get student details
│   │   └─> Returns student info
│   └─> Request 2: Get enrollments
│       ├─> Joins enrollments with courses
│       └─> Returns enrolled courses list
│
└─> FLASK combines data
    ├─> Merges student info and enrollments
    ├─> Calculates total credits
    ├─> Renders student dashboard
    └─> Shows all information in one view
```

### Flow 6: Error Scenarios
```
Scenario: Database Connection Failed
│
├─> User tries to view students
├─> FLASK calls FastAPI
├─> FASTAPI fails to connect to database
│   └─> Returns 500 error with message
└─> FLASK handles error
    ├─> Logs full error for debugging
    ├─> Shows user-friendly error page
    └─> Suggests trying again later

Scenario: Invalid Form Data
│
├─> User submits incomplete form
├─> FLASK does initial validation
│   └─> If fails, shows form errors immediately
├─> If passes, sends to FastAPI
├─> FASTAPI does deeper validation
│   └─> Returns 422 with validation errors
└─> FLASK shows specific field errors
```

## Summary: Division of Responsibilities

### Flask (Frontend) Responsibilities:
1. **User Interface**: Serves HTML pages and handles browser interactions
2. **Session Management**: Maintains user state across requests
3. **Form Handling**: Collects and initially validates user input
4. **API Client**: Makes HTTP requests to FastAPI backend
5. **Template Rendering**: Combines data with HTML templates
6. **User Experience**: Flash messages, redirects, error pages
7. **Static Files**: Serves CSS, JavaScript, and images

### FastAPI (Backend) Responsibilities:
1. **Data API**: Provides RESTful endpoints for data operations
2. **Business Logic**: Enforces rules like enrollment limits
3. **Database Operations**: All SQL queries and transactions
4. **Data Validation**: Schema validation with Pydantic
5. **Data Serialization**: Converts between JSON and Python objects
6. **API Documentation**: Auto-generates API docs
7. **Performance**: Handles concurrent requests efficiently

### When Each is Used:
- **Flask is used when**: User interacts with browser (viewing pages, submitting forms)
- **FastAPI is used when**: Data needs to be created, read, updated, or deleted
- **Both are used together**: On every page load that shows dynamic data