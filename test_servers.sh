#!/bin/bash

echo "Testing Student Enrollment System Servers..."
echo "==========================================="
echo ""

# Test FastAPI backend
echo -n "Testing FastAPI backend (http://localhost:8000): "
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health | grep -q "200"; then
    echo "✓ Running"
    
    # Test a few endpoints
    echo "  Testing endpoints:"
    
    # Test students endpoint
    echo -n "    /students: "
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/students)
    if [ "$STATUS" = "200" ]; then
        echo "✓ OK"
    else
        echo "✗ Failed (Status: $STATUS)"
    fi
    
    # Test courses endpoint
    echo -n "    /courses: "
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/courses)
    if [ "$STATUS" = "200" ]; then
        echo "✓ OK"
    else
        echo "✗ Failed (Status: $STATUS)"
    fi
    
    # Test stats endpoint
    echo -n "    /stats: "
    STATS=$(curl -s http://localhost:8000/stats)
    if [ $? -eq 0 ]; then
        echo "✓ OK"
        echo "    Stats: $STATS"
    else
        echo "✗ Failed"
    fi
else
    echo "✗ Not running"
    echo "  Start with: ./run_backend.sh"
fi

echo ""

# Test Flask frontend
echo -n "Testing Flask frontend (http://localhost:5001): "
if curl -s -L -o /dev/null -w "%{http_code}" http://localhost:5001/ | grep -q "200"; then
    echo "✓ Running"
else
    echo "✗ Not running"
    echo "  Start with: ./run_frontend.sh"
fi

echo ""
echo "==========================================="
echo "To start both servers: ./run_all.sh"
echo "To initialize sample data: python init_sample_data.py"