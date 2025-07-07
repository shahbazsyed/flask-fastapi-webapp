#!/bin/bash

echo "Starting FastAPI Backend Server..."

cd fastapi-backend

# Install dependencies if needed
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
fi

echo "Installing/updating dependencies..."
uv sync

# Run the FastAPI server
echo "Starting FastAPI on http://localhost:8000"
echo "API docs available at http://localhost:8000/docs"
uv run uvicorn main:app --reload --port 8000