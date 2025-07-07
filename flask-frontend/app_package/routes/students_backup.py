"""
Student management routes
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length
import logging

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from api_client import get_api_client, APIError, api_auth_required, handle_api_error

logger = logging.getLogger(__name__)

# Create blueprint
students_bp = Blueprint('students', __name__)


class StudentForm(FlaskForm):
    """Form for creating/editing students"""
    student_id = StringField('Student ID', validators=[
        DataRequired(),
        Length(min=1, max=50)
    ])
    name = StringField('Full Name', validators=[
        DataRequired(),
        Length(min=1, max=100)
    ])
    email = EmailField('Email Address', validators=[
        DataRequired(),
        Email()
    ])
    submit = SubmitField('Save Student')


@students_bp.route('/')
@api_auth_required
@handle_api_error
def index():
    """List all students"""
    api = get_api_client()
    
    # Get query parameters
    search = request.args.get('search', '')
    page = int(request.args.get('page', 1))
    per_page = 20
    
    # Prepare API parameters
    params = {
        'skip': (page - 1) * per_page,
        'limit': per_page
    }
    if search:
        params['search'] = search
    
    # Get students
    students = api.get('/students', params=params)
    
    return render_template('students/index.html', 
                         students=students,
                         search=search,
                         page=page,
                         per_page=per_page)


@students_bp.route('/create', methods=['GET', 'POST'])
@api_auth_required
@handle_api_error
def create():
    """Create a new student"""
    form = StudentForm()
    
    if form.validate_on_submit():
        api = get_api_client()
        
        try:
            student_data = {
                'student_id': form.student_id.data,
                'name': form.name.data,
                'email': form.email.data
            }
            
            student = api.post('/students', json=student_data)
            flash(f'Student {student["name"]} created successfully!', 'success')
            return redirect(url_for('students.view', student_id=student['id']))
            
        except APIError as e:
            if 'already exists' in str(e):
                flash('A student with this ID or email already exists.', 'error')
            else:
                flash(f'Error creating student: {e.message}', 'error')
    
    return render_template('students/form.html', form=form, title='Create Student')


@students_bp.route('/<int:student_id>')
@api_auth_required
@handle_api_error
def view(student_id):
    """View student details"""
    api = get_api_client()
    
    # Get student with enrollments
    student = api.get(f'/students/{student_id}')
    
    # Separate enrollments by status
    active_enrollments = [e for e in student.get('enrollments', []) if e['status'] == 'active']
    completed_enrollments = [e for e in student.get('enrollments', []) if e['status'] == 'completed']
    dropped_enrollments = [e for e in student.get('enrollments', []) if e['status'] == 'dropped']
    
    return render_template('students/view.html',
                         student=student,
                         active_enrollments=active_enrollments,
                         completed_enrollments=completed_enrollments,
                         dropped_enrollments=dropped_enrollments)


@students_bp.route('/<int:student_id>/edit', methods=['GET', 'POST'])
@api_auth_required
@handle_api_error
def edit(student_id):
    """Edit student details"""
    api = get_api_client()
    
    # Get current student data
    student = api.get(f'/students/{student_id}')
    
    form = StudentForm(obj=student)
    form.student_id.render_kw = {'readonly': True}  # Can't change student ID
    
    if form.validate_on_submit():
        try:
            update_data = {
                'name': form.name.data,
                'email': form.email.data
            }
            
            updated_student = api.put(f'/students/{student_id}', json=update_data)
            flash(f'Student {updated_student["name"]} updated successfully!', 'success')
            return redirect(url_for('students.view', student_id=student_id))
            
        except APIError as e:
            if 'already exists' in str(e):
                flash('This email is already used by another student.', 'error')
            else:
                flash(f'Error updating student: {e.message}', 'error')
    
    return render_template('students/form.html', 
                         form=form, 
                         title='Edit Student',
                         student=student)


@students_bp.route('/<int:student_id>/delete', methods=['POST'])
@api_auth_required
@handle_api_error
def delete(student_id):
    """Delete a student"""
    api = get_api_client()
    
    try:
        # Get student info for confirmation message
        student = api.get(f'/students/{student_id}')
        
        # Delete the student
        api.delete(f'/students/{student_id}')
        flash(f'Student {student["name"]} deleted successfully!', 'success')
        
    except APIError as e:
        flash(f'Error deleting student: {e.message}', 'error')
    
    return redirect(url_for('students.index'))