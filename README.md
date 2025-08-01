# API WebApp Example - Student Management System

A full-stack web application demonstrating a student management system with course enrollment functionality. Built with FastAPI (backend) and Flask (frontend).

## Architecture Overview

- **Backend**: FastAPI with SQLAlchemy and SQLite database
- **Frontend**: Flask with Jinja2 templates and Bootstrap UI
- **API Communication**: RESTful API with automatic documentation

## Features

- **Student Management**: Create, view, update, and delete student records
- **Course Management**: Manage course information including schedules and credits
- **Enrollment System**: Enroll students in courses and track grades
- **RESTful API**: Full CRUD operations with OpenAPI documentation
- **Responsive UI**: Bootstrap-based interface for all screen sizes

## Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer and resolver

### Installing uv

```bash
# On macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Project Structure

```
api-webapp-example/
├── fastapi-backend/        # Backend API server
│   ├── app/               # Application code
│   │   ├── models.py      # Database models
│   │   ├── schemas.py     # Pydantic schemas
│   │   ├── database.py    # Database configuration
│   │   └── config.py      # App configuration
│   ├── main.py            # FastAPI application
│   └── pyproject.toml     # Backend dependencies
├── flask-frontend/         # Frontend web application
│   ├── app/               # Application code
│   │   └── routes/        # Route handlers
│   ├── templates/         # Jinja2 templates
│   ├── static/            # CSS and JavaScript
│   ├── api_client.py      # API client wrapper
│   ├── app.py             # Flask application
│   └── pyproject.toml     # Frontend dependencies
├── run_backend.sh         # Start backend server
├── run_frontend.sh        # Start frontend server
├── run_all.sh            # Start both servers
└── init_sample_data.py   # Initialize sample data
```

## Quick Start

### 1. Clone the repository

```bash
git clone <repository-url>
cd api-webapp-example
```

### 2. Start the servers

The easiest way to get started is to run both servers:

```bash
./run_all.sh
```

This will:
- Create virtual environments for both backend and frontend
- Install all dependencies
- Start the FastAPI backend on http://localhost:8000
- Start the Flask frontend on http://localhost:5000

### 3. Initialize sample data (optional)

In a new terminal, run:

```bash
python init_sample_data.py
```

This will populate the database with:
- 8 sample students
- 8 sample courses
- Random enrollments with grades

## Running Individual Components

### Backend Only

```bash
./run_backend.sh
```

- API runs at: http://localhost:8000
- API documentation: http://localhost:8000/docs
- Alternative API docs: http://localhost:8000/redoc

### Frontend Only

```bash
./run_frontend.sh
```

- Web application runs at: http://localhost:5000

## Manual Setup (without scripts)

### Backend Setup

```bash
cd fastapi-backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip sync requirements.txt
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd flask-frontend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
python run.py
```

## API Endpoints

### Students
- `GET /students/` - List all students
- `POST /students/` - Create a new student
- `GET /students/{id}` - Get student details
- `PUT /students/{id}` - Update student
- `DELETE /students/{id}` - Delete student

### Courses
- `GET /courses/` - List all courses
- `POST /courses/` - Create a new course
- `GET /courses/{id}` - Get course details
- `PUT /courses/{id}` - Update course
- `DELETE /courses/{id}` - Delete course

### Enrollments
- `GET /enrollments/` - List all enrollments
- `POST /enrollments/` - Create a new enrollment
- `GET /enrollments/{id}` - Get enrollment details
- `PUT /enrollments/{id}` - Update enrollment (e.g., add grade)
- `DELETE /enrollments/{id}` - Delete enrollment

## Development

### Adding New Features

1. **Backend**: Add new models in `fastapi-backend/app/models.py` and schemas in `schemas.py`
2. **Frontend**: Add new routes in `flask-frontend/app/routes/` and templates in `templates/`

### Database Schema

The application uses SQLite with three main tables:

- **students**: id, name, email, age, major
- **courses**: id, name, code, credits, instructor, schedule, description
- **enrollments**: id, student_id, course_id, enrollment_date, grade

### Testing the API

You can test the API using the included test script:

```bash
cd fastapi-backend
python test_api.py
```

Or use the interactive API documentation at http://localhost:8000/docs

## Troubleshooting

### Port Already in Use

If you get a "port already in use" error:

```bash
# Kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill process on port 5000 (frontend)
lsof -ti:5000 | xargs kill -9
```

### Database Issues

To reset the database:

```bash
cd fastapi-backend
rm -f student_management.db
# Restart the backend server
```

### Dependency Issues

If you encounter dependency conflicts:

```bash
# Backend
cd fastapi-backend
rm -rf .venv uv.lock
uv venv
uv pip sync requirements.txt

# Frontend
cd flask-frontend
rm -rf .venv uv.lock
uv venv
uv pip install -e .
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.