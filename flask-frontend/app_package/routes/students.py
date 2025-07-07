"""
Student management routes for Flask frontend
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from api_client import get_api_client, handle_api_error, APIError
import logging

logger = logging.getLogger(__name__)

students_bp = Blueprint('students', __name__)


@students_bp.route('/')
@handle_api_error
def list_students():
    """List all students with pagination and search"""
    client = get_api_client()
    
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    search = request.args.get('search', '')
    
    # Calculate skip value for pagination
    skip = (page - 1) * per_page
    
    # Fetch students from API
    params = {
        'skip': skip,
        'limit': per_page
    }
    if search:
        params['search'] = search
    
    try:
        response = client.get('/students', params=params)
        
        # Extract data from paginated response
        students = response.get('items', [])
        total = response.get('total', 0)
        
        # Calculate pagination info
        has_next = (page * per_page) < total
        has_prev = page > 1
        total_pages = (total + per_page - 1) // per_page if per_page > 0 else 0
        
        return render_template('students/list.html',
                             students=students,
                             page=page,
                             per_page=per_page,
                             search=search,
                             has_next=has_next,
                             has_prev=has_prev,
                             total=total,
                             total_pages=total_pages)
    except APIError as e:
        logger.error(f"Error fetching students: {e}")
        flash('Error fetching students. Please try again.', 'error')
        return render_template('students/list.html', students=[], page=1, per_page=per_page)


@students_bp.route('/create', methods=['GET', 'POST'])
@handle_api_error
def create_student():
    """Create a new student"""
    if request.method == 'POST':
        # Get form data
        student_id = request.form.get('student_id', '').strip()
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        
        # Basic validation
        errors = []
        if not student_id:
            errors.append('Student ID is required')
        if not name:
            errors.append('Name is required')
        if not email:
            errors.append('Email is required')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('students/create.html',
                                 student_id=student_id,
                                 name=name,
                                 email=email)
        
        # Create student via API
        client = get_api_client()
        try:
            student = client.post('/students', json={
                'student_id': student_id,
                'name': name,
                'email': email
            })
            
            flash(f'Student "{student["name"]}" created successfully!', 'success')
            return redirect(url_for('students.view_student', student_id=student['id']))
            
        except APIError as e:
            logger.error(f"Error creating student: {e}")
            flash(f'Error creating student: {e.message}', 'error')
            return render_template('students/create.html',
                                 student_id=student_id,
                                 name=name,
                                 email=email)
    
    return render_template('students/create.html')


@students_bp.route('/<int:student_id>')
@handle_api_error
def view_student(student_id):
    """View a single student's details"""
    client = get_api_client()
    
    try:
        student = client.get(f'/students/{student_id}')
        
        # Separate active and inactive enrollments
        active_enrollments = [e for e in student.get('enrollments', []) if e['status'] == 'active']
        inactive_enrollments = [e for e in student.get('enrollments', []) if e['status'] != 'active']
        
        return render_template('students/view.html',
                             student=student,
                             active_enrollments=active_enrollments,
                             inactive_enrollments=inactive_enrollments)
    except APIError as e:
        if e.status_code == 404:
            flash('Student not found', 'error')
            return redirect(url_for('students.list_students'))
        raise


@students_bp.route('/<int:student_id>/edit', methods=['GET', 'POST'])
@handle_api_error
def edit_student(student_id):
    """Edit a student's information"""
    client = get_api_client()
    
    # Fetch current student data
    try:
        student = client.get(f'/students/{student_id}')
    except APIError as e:
        if e.status_code == 404:
            flash('Student not found', 'error')
            return redirect(url_for('students.list_students'))
        raise
    
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        
        # Basic validation
        errors = []
        if not name:
            errors.append('Name is required')
        if not email:
            errors.append('Email is required')
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('students/edit.html',
                                 student=student,
                                 name=name,
                                 email=email)
        
        # Update student via API
        update_data = {}
        if name != student['name']:
            update_data['name'] = name
        if email != student['email']:
            update_data['email'] = email
        
        if update_data:
            try:
                updated_student = client.put(f'/students/{student_id}', json=update_data)
                flash('Student updated successfully!', 'success')
                return redirect(url_for('students.view_student', student_id=student_id))
                
            except APIError as e:
                logger.error(f"Error updating student: {e}")
                flash(f'Error updating student: {e.message}', 'error')
                return render_template('students/edit.html',
                                     student=student,
                                     name=name,
                                     email=email)
        else:
            flash('No changes made', 'info')
            return redirect(url_for('students.view_student', student_id=student_id))
    
    return render_template('students/edit.html', student=student)


@students_bp.route('/<int:student_id>/delete', methods=['POST'])
@handle_api_error
def delete_student(student_id):
    """Delete a student"""
    client = get_api_client()
    
    try:
        # First fetch the student to get their name for the success message
        student = client.get(f'/students/{student_id}')
        student_name = student['name']
        
        # Delete the student
        client.delete(f'/students/{student_id}')
        
        flash(f'Student "{student_name}" deleted successfully!', 'success')
        return redirect(url_for('students.list_students'))
        
    except APIError as e:
        if e.status_code == 404:
            flash('Student not found', 'error')
        else:
            logger.error(f"Error deleting student: {e}")
            flash(f'Error deleting student: {e.message}', 'error')
        
        return redirect(url_for('students.list_students'))


@students_bp.route('/<int:student_id>/enrollments')
@handle_api_error
def student_enrollments(student_id):
    """View a student's enrollments"""
    client = get_api_client()
    
    try:
        # Fetch student details
        student = client.get(f'/students/{student_id}')
        
        # Fetch enrollments for this student
        enrollments_response = client.get(f'/enrollments/student/{student_id}')
        enrollments = enrollments_response.get('items', [])
        
        # Separate by status
        active_enrollments = [e for e in enrollments if e['status'] == 'active']
        completed_enrollments = [e for e in enrollments if e['status'] == 'completed']
        dropped_enrollments = [e for e in enrollments if e['status'] == 'dropped']
        
        return render_template('students/enrollments.html',
                             student=student,
                             active_enrollments=active_enrollments,
                             completed_enrollments=completed_enrollments,
                             dropped_enrollments=dropped_enrollments)
                             
    except APIError as e:
        if e.status_code == 404:
            flash('Student not found', 'error')
            return redirect(url_for('students.list_students'))
        raise


# Alias for compatibility with existing navigation
index = list_students