"""
Flask application initialization and configuration
"""
import os
from flask import Flask, render_template, flash, redirect, url_for, session
from flask_session import Session
from datetime import timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    """Application factory pattern for Flask app creation"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Session configuration
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = os.path.join(os.path.dirname(__file__), '.flask_session')
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_KEY_PREFIX'] = 'flask_frontend:'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
    
    # Template and static directories configuration
    app.template_folder = 'templates'
    app.static_folder = 'static'
    
    # API configuration
    app.config['API_BASE_URL'] = os.environ.get('API_BASE_URL', 'http://localhost:8000')
    app.config['API_TIMEOUT'] = int(os.environ.get('API_TIMEOUT', 30))
    
    # Initialize Flask-Session
    Session(app)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        flash('Page not found', 'error')
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f'Internal error: {error}')
        flash('An internal error occurred', 'error')
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        logger.error(f'Unhandled exception: {error}')
        flash('An unexpected error occurred', 'error')
        return render_template('errors/500.html'), 500
    
    # Context processors
    @app.context_processor
    def inject_globals():
        """Inject global variables into all templates"""
        return {
            'api_base_url': app.config['API_BASE_URL'],
            'app_name': 'Flask Frontend'
        }
    
    # Basic routes
    @app.route('/')
    def index():
        """Home page"""
        return render_template('index.html')
    
    @app.route('/health')
    def health():
        """Health check endpoint"""
        return {'status': 'healthy', 'app': 'flask-frontend'}, 200
    
    # Register blueprints
    # Authentication blueprint removed - no longer needed
    # from app_package.auth import auth_bp
    # app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app_package.routes.students import students_bp
    app.register_blueprint(students_bp, url_prefix='/students')
    
    from app_package.routes.courses import courses_bp
    app.register_blueprint(courses_bp, url_prefix='/courses')
    
    from app_package.routes.enrollments import enrollments_bp
    app.register_blueprint(enrollments_bp, url_prefix='/enrollments')
    
    return app


# Create app instance for Flask CLI
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)