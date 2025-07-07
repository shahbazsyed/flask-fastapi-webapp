#!/usr/bin/env python
"""
Development server runner for Flask application
"""
import os
from dotenv import load_dotenv
from app import app

# Load environment variables
load_dotenv()

if __name__ == '__main__':
    # Get configuration from environment
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    
    print(f"Starting Flask application on {host}:{port}")
    print(f"Debug mode: {debug}")
    print(f"API URL: {app.config['API_BASE_URL']}")
    
    # Run the application
    app.run(
        debug=debug,
        host=host,
        port=port
    )