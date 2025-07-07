"""
Database initialization script
"""
from .database import engine, Base
from .models import Student, Course, Enrollment


def init_db():
    """
    Initialize database by creating all tables
    """
    # Import all models to ensure they are registered with Base
    # This is important for Base.metadata.create_all to work
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def drop_db():
    """
    Drop all database tables (use with caution!)
    """
    Base.metadata.drop_all(bind=engine)
    print("Database tables dropped!")


if __name__ == "__main__":
    # If run directly, initialize the database
    init_db()