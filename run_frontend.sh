#!/bin/bash

echo "Starting Flask Frontend Server..."

cd flask-frontend

# Install dependencies if needed
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
fi

echo "Installing/updating dependencies..."
uv sync

# Run the Flask server
echo "Starting Flask on http://localhost:5001"
export FLASK_DEBUG=True
export FLASK_PORT=5001
uv run python run.py