#!/bin/bash

# Check Status Script
# This script checks if the backend and frontend servers are running

echo "API WebApp Status Check"
echo "======================"
echo ""

# Check backend
echo -n "Backend API (port 8000): "
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health | grep -q "200"; then
    echo "✓ Running"
    echo "  - API Docs: http://localhost:8000/docs"
else
    echo "✗ Not running"
fi

# Check frontend
echo -n "Frontend Web App (port 5000): "
if curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/ | grep -q "200\|302"; then
    echo "✓ Running"
    echo "  - Web App: http://localhost:5000"
else
    echo "✗ Not running"
fi

# Check database
echo -n "Database: "
if [ -f "fastapi-backend/student_management.db" ]; then
    echo "✓ Exists"
    # Get record counts if backend is running
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health | grep -q "200"; then
        STUDENTS=$(curl -s http://localhost:8000/students/ | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "?")
        COURSES=$(curl -s http://localhost:8000/courses/ | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "?")
        ENROLLMENTS=$(curl -s http://localhost:8000/enrollments/ | python3 -c "import sys, json; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "?")
        echo "  - Students: $STUDENTS"
        echo "  - Courses: $COURSES"
        echo "  - Enrollments: $ENROLLMENTS"
    fi
else
    echo "✗ Not found"
fi

echo ""
echo "Quick Actions:"
echo "  - Start all servers: ./run_all.sh"
echo "  - Start backend only: ./run_backend.sh"
echo "  - Start frontend only: ./run_frontend.sh"
echo "  - Initialize sample data: python init_sample_data.py"