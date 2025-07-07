# Student Enrollment System - Complete Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Components](#architecture-components)
3. [Script Connections and Flow](#script-connections-and-flow)
4. [Backend Scripts (FastAPI)](#backend-scripts-fastapi)
5. [Frontend Scripts (Flask)](#frontend-scripts-flask)
6. [Templates and UI Components](#templates-and-ui-components)
7. [Utility Scripts](#utility-scripts)
8. [Data Flow Examples](#data-flow-examples)

## System Overview

The Student Enrollment System follows a two-server architecture as described in `architecture.md`:

```
User Browser <--HTML--> Flask Server <--JSON API--> FastAPI Server <--SQL--> Database
```

- **FastAPI Backend (Port 8000)**: Handles all data operations, business logic, and database interactions
- **Flask Frontend (Port 5001)**: Manages user interface, renders HTML templates, and acts as an API client
- **SQLite Database**: Stores all persistent data (students, courses, enrollments)

## Architecture Components

### 1. Backend Components (FastAPI)

The backend is located in `/fastapi-backend/` and consists of:

- **API Server**: RESTful endpoints for data operations
- **Database Layer**: SQLAlchemy ORM for database interactions
- **Validation Layer**: Pydantic schemas for data validation
- **Business Logic**: Enrollment constraints, course capacity management

### 2. Frontend Components (Flask)

The frontend is located in `/flask-frontend/` and consists of:

- **Web Server**: Serves HTML pages to browsers
- **API Client**: Makes HTTP requests to FastAPI backend
- **Template Engine**: Jinja2 for dynamic HTML generation
- **Session Management**: Handles user state across requests

## Script Connections and Flow

### Startup Scripts

1. **`run_backend.sh`**
   - Purpose: Starts the FastAPI backend server
   - Actions:
     - Creates virtual environment if needed
     - Installs dependencies via `uv sync`
     - Runs `uvicorn main:app --reload --port 8000`
   - Output: FastAPI server accessible at http://localhost:8000

2. **`run_frontend.sh`**
   - Purpose: Starts the Flask frontend server
   - Actions:
     - Creates virtual environment if needed
     - Installs dependencies via `uv sync`
     - Sets environment variables (FLASK_DEBUG=True, FLASK_PORT=5001)
     - Runs `python run.py`
   - Output: Flask server accessible at http://localhost:5001

3. **`run_all.sh`**
   - Purpose: Starts both servers simultaneously
   - Actions:
     - Executes `run_backend.sh` in background
     - Waits 3 seconds for backend to start
     - Executes `run_frontend.sh` in background
     - Sets up cleanup trap for Ctrl+C
   - Output: Both servers running with process management

4. **`test_servers.sh`**
   - Purpose: Checks if servers are running
   - Actions:
     - Tests backend health endpoint
     - Tests frontend availability
     - Checks database existence
     - Displays statistics if available

5. **`check_status.sh`**
   - Purpose: Quick status check of the system
   - Actions:
     - Verifies backend API status
     - Verifies frontend web app status
     - Shows database record counts
     - Provides quick action hints

## Backend Scripts (FastAPI)

### Main Application (`/fastapi-backend/main.py`)

**Purpose**: Core FastAPI application with all API endpoints

**Key Components**:
1. **Application Setup** (lines 1-37):
   ```python
   app = FastAPI(
       title="Student Enrollment API",
       description="RESTful API for managing students, courses, and enrollments",
       version="1.0.0"
   )
   ```
   - Configures CORS for Flask frontend access
   - Creates database tables on startup

2. **Student Endpoints** (lines 47-175):
   - `GET /students` - List with pagination and search
   - `POST /students` - Create with validation
   - `GET /students/{id}` - Get with enrollments
   - `PUT /students/{id}` - Update student info
   - `DELETE /students/{id}` - Remove student

3. **Course Endpoints** (lines 177-331):
   - `GET /courses` - List with filtering
   - `POST /courses` - Create new course
   - `GET /courses/{id}` - Get course details
   - `GET /courses/{id}/students` - List enrolled students
   - `PUT /courses/{id}` - Update course
   - `DELETE /courses/{id}` - Delete (checks enrollments)

4. **Enrollment Endpoints** (lines 333-515):
   - `POST /enrollments` - Enroll student (checks capacity)
   - `GET /enrollments` - List all enrollments
   - `GET /enrollments/student/{id}` - Student's enrollments
   - `GET /enrollments/course/{id}` - Course's enrollments
   - `PUT /enrollments/{id}` - Update status
   - `DELETE /enrollments/{id}` - Remove enrollment

5. **Utility Endpoints** (lines 517-535):
   - `GET /health` - Health check
   - `GET /stats` - System statistics

### Database Models (`/fastapi-backend/app/models.py`)

**Purpose**: SQLAlchemy ORM models defining database structure

**Models**:
1. **Student**:
   - Fields: id, student_id (unique), name, email (unique), created_at
   - Relationships: Has many enrollments (cascade delete)
   
2. **Course**:
   - Fields: id, course_code (unique), name, description, credits, max_students
   - Properties: enrolled_count, available_seats (calculated)
   - Relationships: Has many enrollments

3. **Enrollment**:
   - Fields: id, student_id (FK), course_id (FK), enrollment_date, status
   - Unique constraint: (student_id, course_id)
   - Status values: 'active', 'dropped', 'completed'

### Schemas (`/fastapi-backend/app/schemas.py`)

**Purpose**: Pydantic models for request/response validation

**Key Schemas**:
1. **Student Schemas**:
   - `StudentCreate`: For new students (student_id, name, email)
   - `StudentRead`: For responses (includes id, created_at)
   - `StudentUpdate`: For updates (all fields optional)
   - `StudentWithEnrollments`: Includes enrollment list

2. **Course Schemas**:
   - `CourseCreate`: For new courses
   - `CourseRead`: Includes calculated fields
   - `CourseUpdate`: Partial updates
   - `CourseWithStudents`: Includes enrolled students

3. **Enrollment Schemas**:
   - `EnrollmentCreate`: Just student_id and course_id
   - `EnrollmentRead`: Full enrollment data
   - `EnrollmentUpdate`: Status changes
   - `EnrollmentWithCourse/Student`: Includes related data

4. **Utility Schemas**:
   - `PaginatedResponse[T]`: Generic pagination wrapper
   - `SuccessResponse`: Standard success format
   - `ErrorResponse`: Standard error format

### Database Configuration (`/fastapi-backend/app/database.py`)

**Purpose**: Database connection and session management

**Components**:
- SQLite connection string
- SQLAlchemy engine creation
- Session factory configuration
- `get_db()` dependency for request-scoped sessions

### Configuration (`/fastapi-backend/app/config.py`)

**Purpose**: Application settings management

**Settings**:
- App name and version
- Database URL
- CORS origins (includes ports 5000 and 5001)
- Pagination defaults
- Environment configuration

## Frontend Scripts (Flask)

### Main Application (`/flask-frontend/app.py`)

**Purpose**: Flask application initialization and configuration

**Key Components**:
1. **Application Factory** (`create_app()` function):
   - Session configuration (filesystem-based)
   - Template and static folder setup
   - API base URL configuration
   - Error handlers (404, 500)
   
2. **Context Processors** (lines 60-67):
   - Provides `app_name` globally to templates
   
3. **Basic Routes**:
   - `/` - Home page (renders index.html)
   - `/health` - Health check endpoint
   
4. **Blueprint Registration**:
   - Students blueprint at `/students`
   - Courses blueprint at `/courses`
   - Enrollments blueprint at `/enrollments`

### API Client (`/flask-frontend/api_client.py`)

**Purpose**: Centralized API communication with FastAPI backend

**Key Components**:
1. **APIClient Class**:
   - Base URL configuration (http://localhost:8000)
   - Session management with connection pooling
   - Methods for all HTTP verbs (GET, POST, PUT, PATCH, DELETE)
   - Automatic JSON serialization/deserialization
   - Comprehensive error handling

2. **Error Handling**:
   - `APIError` custom exception class
   - `handle_api_error` decorator for routes
   - Automatic flash messages for errors
   - Redirect to home on API failures

3. **Singleton Pattern**:
   - `get_api_client()` returns shared instance
   - Efficient connection reuse

### Route Blueprints

#### Students Blueprint (`/flask-frontend/app_package/routes/students.py`)

**Routes**:
1. `list_students()` - `/students/`
   - Gets paginated student list from API
   - Supports search functionality
   - Renders `students/index.html`

2. `create()` - `/students/create`
   - GET: Shows creation form
   - POST: Sends data to API, redirects on success
   - Uses WTForms for validation

3. `view()` - `/students/<id>`
   - Fetches student details with enrollments
   - Renders `students/view.html`

4. `edit()` - `/students/<id>/edit`
   - GET: Shows edit form with current data
   - POST: Updates via API
   - Renders `students/form.html`

5. `delete()` - `/students/<id>/delete`
   - POST only, deletes via API
   - Redirects to student list

6. `enrollments()` - `/students/<id>/enrollments`
   - Shows all enrollments for a student
   - Renders `students/enrollments.html`

#### Courses Blueprint (`/flask-frontend/app_package/routes/courses.py`)

**Routes**:
1. `list_courses()` - `/courses/`
   - Paginated course listing
   - Search and filter capabilities
   - Available seats filter option
   - Renders `courses/index.html`

2. `create()` - `/courses/new`
   - Course creation form and processing
   - Renders `courses/create.html`

3. `view_course()` - `/courses/<id>`
   - Course details with enrolled students
   - Enrollment/unenrollment forms
   - Renders `courses/detail.html`

4. `edit()` - `/courses/<id>/edit`
   - Course editing functionality
   - Renders `courses/edit.html`

5. `delete()` - `/courses/<id>/delete`
   - Course deletion with enrollment check

6. `enroll()` - `/courses/<id>/enroll`
   - POST: Enrolls student in course
   - Validates capacity constraints

7. `unenroll()` - `/courses/<id>/unenroll`
   - POST: Removes student from course

#### Enrollments Blueprint (`/flask-frontend/app_package/routes/enrollments.py`)

**Routes**:
1. `index()` - `/enrollments/`
   - Admin view of all enrollments
   - Status filtering (active/dropped/completed)
   - Renders `enrollments/index.html`

2. `student_enrollments()` - `/enrollments/student/<id>`
   - Shows specific student's enrollments
   - Allows dropping courses
   - Renders `enrollments/student.html`

3. `course_enrollments()` - `/enrollments/course/<id>`
   - Shows all students in a course
   - Renders `enrollments/course.html`

4. `enroll()` - `/enrollments/enroll`
   - POST: Creates new enrollment

5. `drop()` - `/enrollments/drop`
   - POST: Sets enrollment status to 'dropped'

6. `complete()` - `/enrollments/complete/<id>`
   - POST: Marks enrollment as completed

7. `delete()` - `/enrollments/delete/<id>`
   - POST: Permanently removes enrollment

### Support Scripts

#### `run.py`
**Purpose**: Development server runner
- Loads environment variables
- Imports app instance from app.py
- Configures host, port, and debug mode
- Starts Flask development server

## Templates and UI Components

### Base Template (`/templates/base.html`)

**Purpose**: Master layout template for all pages

**Components**:
1. **HTML Structure**:
   - Bootstrap 5 CSS framework
   - Bootstrap Icons library
   - Custom CSS (`/static/css/style.css`)
   - Responsive meta viewport

2. **Navigation Bar** (lines 21-44):
   - Dark theme navbar
   - Brand link to home
   - Navigation links: Home, Students, Courses, Enrollments
   - Mobile-responsive collapse menu

3. **Flash Messages** (lines 46-59):
   - Auto-dismiss after 5 seconds
   - Different styles for success/error/warning/info
   - JavaScript for fade-out effect

4. **Content Blocks**:
   - `{% block title %}` - Page-specific titles
   - `{% block content %}` - Main page content
   - `{% block extra_css %}` - Additional styles
   - `{% block extra_js %}` - Additional scripts

### Home Page (`/templates/index.html`)

**Purpose**: Landing page with system overview

**Sections**:
1. **Hero Section**: Welcome message and description
2. **Quick Links Cards** (3 columns):
   - Students card with link to student list
   - Courses card with link to course catalog
   - Enrollments card with link to enrollment management
3. **System Statistics**: 
   - Displays total counts from API `/stats` endpoint
   - Shows API connection status

### Student Templates

#### `/templates/students/index.html`
**Purpose**: Student listing page
- Search bar for name/email/ID filtering
- Table with student information
- Action buttons: View, Enrollments, Edit
- Pagination controls
- "Add New Student" button

#### `/templates/students/view.html`
**Purpose**: Individual student details
- Student information display
- Enrolled courses table
- Quick stats (total courses, credits)
- Edit and back navigation buttons

#### `/templates/students/form.html`
**Purpose**: Reusable form for create/edit
- Student ID field (disabled on edit)
- Name and email inputs
- Form validation display
- Submit and cancel buttons

#### `/templates/students/create.html`
**Purpose**: Student creation page
- Extends form.html
- Sets form action to create route

#### `/templates/students/edit.html`
**Purpose**: Student editing page
- Extends form.html
- Pre-fills current values
- Sets form action to edit route

#### `/templates/students/enrollments.html`
**Purpose**: Student's enrollment history
- Shows all courses student is/was enrolled in
- Status badges (active/dropped/completed)
- Drop course buttons for active enrollments
- Credit summary

### Course Templates

#### `/templates/courses/index.html`
**Purpose**: Course catalog listing
- Search bar with course filtering
- "Available only" checkbox filter
- Course cards showing:
  - Course code and name
  - Description preview
  - Credits and capacity
  - Enrollment progress bar
  - Action buttons

#### `/templates/courses/detail.html`
**Purpose**: Course details page
- Full course information
- Enrollment statistics and progress bar
- Enrolled students table
- Enrollment form (requires student ID input)
- Edit course button

#### `/templates/courses/create.html`
**Purpose**: New course creation
- Course code, name, description fields
- Credits selector (1-6)
- Maximum students input
- Form validation

#### `/templates/courses/edit.html`
**Purpose**: Course editing
- Pre-filled form fields
- Current enrollment count display
- Prevents reducing capacity below enrolled count

#### `/templates/courses/form.html`
**Purpose**: Shared course form template
- Reusable form structure
- WTForms integration
- Bootstrap styling

### Enrollment Templates

#### `/templates/enrollments/index.html`
**Purpose**: Admin view of all enrollments
- Status filter buttons (All/Active/Dropped/Completed)
- Enrollment table with:
  - Student name and ID
  - Course name and code
  - Enrollment date
  - Status with color coding
  - Action buttons
- Pagination support

#### `/templates/enrollments/student.html`
**Purpose**: Student-specific enrollment view
- Student header information
- Active enrollments with drop buttons
- Completed enrollments history
- Total credits calculation
- Link to enroll in new courses

#### `/templates/enrollments/course.html`
**Purpose**: Course-specific enrollment view
- Course header with capacity info
- Enrolled students table
- Enrollment dates
- Status indicators
- Unenroll options

### Error Templates

#### `/templates/errors/404.html`
**Purpose**: Page not found error
- User-friendly 404 message
- Link back to home page
- Maintains site navigation

#### `/templates/errors/500.html`
**Purpose**: Internal server error
- Generic error message
- Avoids exposing technical details
- Home page redirect option

### Static Files

#### `/static/css/style.css`
**Purpose**: Custom CSS styles
- Card hover effects
- Progress bar animations
- Alert transitions
- Responsive adjustments
- Loading spinner styles

#### `/static/js/main.js`
**Purpose**: Client-side JavaScript
- Auto-dismiss flash messages
- Form validation helpers
- AJAX request handlers
- Loading state management
- Delete confirmation modals

## Utility Scripts

### `init_sample_data.py`

**Purpose**: Initialize database with test data

**Process**:
1. Checks API health before proceeding
2. Creates 8 sample students
3. Creates 8 sample courses
4. Randomly enrolls students (2-5 courses each)
5. Handles existing data gracefully
6. Displays final statistics

**Data Created**:
- Students: Alice Johnson, Bob Smith, Carol Davis, etc.
- Courses: CS101, CS201, MATH101, PHYS101, etc.
- Random enrollments respecting capacity limits

## Data Flow Examples

### Example 1: Viewing Student List

1. **User** navigates to http://localhost:5001/students
2. **Flask** routes to `students.list_students()`
3. **Route** calls `api_client.get('/students?skip=0&limit=20')`
4. **API Client** sends HTTP GET to FastAPI
5. **FastAPI** queries database via SQLAlchemy
6. **Database** returns student records
7. **FastAPI** serializes to JSON with Pydantic
8. **API Client** receives JSON response
9. **Route** passes data to template
10. **Template** renders HTML table
11. **Browser** displays student list

### Example 2: Enrolling in a Course

1. **User** fills enrollment form on course detail page
2. **Form** submits POST to `/courses/{id}/enroll`
3. **Flask** validates form data
4. **Route** prepares enrollment data
5. **API Client** sends POST to `/enrollments`
6. **FastAPI** validates:
   - Student exists
   - Course exists
   - Course has capacity
   - Not already enrolled
7. **Database** creates enrollment record
8. **FastAPI** returns success response
9. **Flask** sets success flash message
10. **Route** redirects to course page
11. **Browser** shows updated enrollment count

### Example 3: Error Handling Flow

1. **User** tries to enroll in full course
2. **Flask** sends enrollment request
3. **FastAPI** checks capacity constraint
4. **FastAPI** returns 400 error: "Course is full"
5. **API Client** raises APIError
6. **Error Handler** catches exception
7. **Flask** sets error flash message
8. **Route** redirects to previous page
9. **Browser** displays error message

## Configuration Files

### `/fastapi-backend/pyproject.toml`
- Project metadata
- Dependencies: fastapi, uvicorn, sqlalchemy, pydantic, email-validator
- Build configuration

### `/flask-frontend/pyproject.toml`
- Project metadata  
- Dependencies: flask, flask-session, flask-wtf, requests, email-validator
- Build configuration

### `/flask-frontend/.env`
- Environment variables
- API base URL
- Secret keys
- Debug settings

## Security Considerations

1. **CORS Configuration**: Restricted to specific origins
2. **Input Validation**: Both frontend (WTForms) and backend (Pydantic)
3. **SQL Injection Prevention**: SQLAlchemy parameterized queries
4. **Error Information**: Generic errors in production
5. **Session Security**: Signed sessions with secret key

## Performance Features

1. **Pagination**: All list endpoints support pagination
2. **Connection Pooling**: API client reuses connections
3. **Lazy Loading**: Relationships loaded on demand
4. **Indexed Fields**: Database indexes on frequently queried fields
5. **Caching**: 15-minute cache for static content

## Monitoring and Debugging

1. **Health Endpoints**: Both servers have `/health` endpoints
2. **Logging**: Comprehensive logging at all layers
3. **Error Tracking**: Detailed error messages in development
4. **Statistics Endpoint**: Real-time system metrics
5. **Debug Mode**: Auto-reload on code changes

This completes the comprehensive documentation of the Student Enrollment System, detailing every script, template, and their interconnections following the architecture defined in architecture.md.