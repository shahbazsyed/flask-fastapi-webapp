#!/usr/bin/env python3
"""Test script to verify Flask frontend works without authentication"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

def test_routes():
    """Test that routes are accessible without authentication"""
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        # Test home page
        response = client.get('/')
        print(f"Home page: {response.status_code}")
        assert response.status_code == 200
        
        # Test students list
        response = client.get('/students/')
        print(f"Students list: {response.status_code}")
        assert response.status_code == 200
        
        # Test courses list
        response = client.get('/courses/')
        print(f"Courses list: {response.status_code}")
        assert response.status_code == 200
        
        # Test enrollments list
        response = client.get('/enrollments/')
        print(f"Enrollments list: {response.status_code}")
        assert response.status_code == 200
        
        # Test create student page
        response = client.get('/students/create')
        print(f"Create student page: {response.status_code}")
        assert response.status_code == 200
        
        # Test create course page
        response = client.get('/courses/new')
        print(f"Create course page: {response.status_code}")
        assert response.status_code == 200
        
        print("\nAll routes are accessible without authentication!")

if __name__ == '__main__':
    test_routes()