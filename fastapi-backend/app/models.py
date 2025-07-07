"""
SQLAlchemy models for the student enrollment system
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Student(Base):
    """Student model"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship with enrollments
    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")


class Course(Base):
    """Course model"""
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    course_code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    credits = Column(Integer, nullable=False)
    max_students = Column(Integer, nullable=False, default=30)
    
    # Relationship with enrollments
    enrollments = relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")
    
    @property
    def enrolled_count(self):
        """Get the number of enrolled students"""
        return len([e for e in self.enrollments if e.status == "active"])
    
    @property
    def available_seats(self):
        """Calculate available seats"""
        return self.max_students - self.enrolled_count


class Enrollment(Base):
    """Enrollment model - junction table between students and courses"""
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrollment_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), nullable=False, default="active")  # active, dropped, completed
    
    # Relationships
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    
    # Ensure a student can only be enrolled once in a course
    __table_args__ = (
        UniqueConstraint('student_id', 'course_id', name='_student_course_uc'),
    )