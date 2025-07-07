#!/bin/bash

echo "Starting Student Enrollment System..."
echo "=================================="

# Function to cleanup on exit
cleanup() {
    echo -e "\n\nStopping all servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "All servers stopped."
    exit 0
}

# Set up trap for cleanup
trap cleanup INT TERM EXIT

# Start FastAPI backend
echo "Starting FastAPI backend..."
./run_backend.sh &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Start Flask frontend
echo -e "\n\nStarting Flask frontend..."
./run_frontend.sh &
FRONTEND_PID=$!

# Wait a bit for frontend to start
sleep 3

echo -e "\n\n=================================="
echo "Both servers are now running!"
echo "FastAPI backend: http://localhost:8000 (API docs: http://localhost:8000/docs)"
echo "Flask frontend: http://localhost:5001"
echo -e "\nPress Ctrl+C to stop all servers"
echo "=================================="

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID