"""
Enrollment management routes
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_wtf import FlaskForm
from wtforms import SelectField, HiddenField, SubmitField
from wtforms.validators import DataRequired
import logging

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from api_client import get_api_client, APIError, handle_api_error

logger = logging.getLogger(__name__)

# Create blueprint
enrollments_bp = Blueprint('enrollments', __name__)


class EnrollmentForm(FlaskForm):
    """Form for enrolling in a course"""
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    student_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Enroll')


class DropCourseForm(FlaskForm):
    """Form for dropping a course"""
    enrollment_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Drop Course')


@enrollments_bp.route('/')
@handle_api_error
def index():
    """List all enrollments (admin view)"""
    api = get_api_client()
    
    # Get query parameters
    status = request.args.get('status')
    page = int(request.args.get('page', 1))
    per_page = 20
    
    # Prepare API parameters
    params = {
        'skip': (page - 1) * per_page,
        'limit': per_page
    }
    if status:
        params['status'] = status
    
    # Get enrollments
    response = api.get('/enrollments', params=params)
    
    # Extract data from paginated response
    enrollments = response.get('items', [])
    total = response.get('total', 0)
    
    # Get student and course details for each enrollment
    for enrollment in enrollments:
        try:
            enrollment['student'] = api.get(f'/students/{enrollment["student_id"]}')
            enrollment['course'] = api.get(f'/courses/{enrollment["course_id"]}')
        except APIError:
            # If we can't get details, use IDs
            enrollment['student'] = {'name': f'Student {enrollment["student_id"]}', 'id': enrollment['student_id']}
            enrollment['course'] = {'name': f'Course {enrollment["course_id"]}', 'id': enrollment['course_id']}
    
    # Calculate pagination info
    total_pages = (total + per_page - 1) // per_page if per_page > 0 else 0
    has_next = (page * per_page) < total
    has_prev = page > 1
    
    return render_template('enrollments/index.html', 
                         enrollments=enrollments,
                         status=status,
                         page=page,
                         per_page=per_page,
                         total=total,
                         total_pages=total_pages,
                         has_next=has_next,
                         has_prev=has_prev)


@enrollments_bp.route('/student/<int:student_id>')
@handle_api_error
def student_enrollments(student_id):
    """View enrollments for a specific student"""
    api = get_api_client()
    
    # Get student details
    student = api.get(f'/students/{student_id}')
    
    # Get student enrollments
    status = request.args.get('status', 'active')
    params = {'status': status} if status != 'all' else {}
    response = api.get(f'/enrollments/student/{student_id}', params=params)
    enrollments = response.get('items', [])
    
    # Get available courses for enrollment
    courses_response = api.get('/courses', params={'limit': 1000})  # Get all courses
    all_courses = courses_response.get('items', [])
    enrolled_course_ids = [e['course_id'] for e in enrollments if e['status'] == 'active']
    available_courses = [c for c in all_courses if c['id'] not in enrolled_course_ids and c['available_seats'] > 0]
    
    # Create enrollment form
    form = EnrollmentForm()
    form.course_id.choices = [(c['id'], f"{c['course_code']} - {c['name']} ({c['available_seats']} seats)") 
                             for c in available_courses]
    form.student_id.data = student_id
    
    # Create drop forms for each enrollment
    drop_forms = {}
    for enrollment in enrollments:
        if enrollment['status'] == 'active':
            drop_form = DropCourseForm()
            drop_form.enrollment_id.data = enrollment['id']
            drop_forms[enrollment['id']] = drop_form
    
    return render_template('enrollments/student.html',
                         student=student,
                         enrollments=enrollments,
                         form=form,
                         drop_forms=drop_forms,
                         status=status,
                         available_courses=available_courses)


@enrollments_bp.route('/course/<int:course_id>')
@handle_api_error
def course_enrollments(course_id):
    """View enrollments for a specific course"""
    api = get_api_client()
    
    # Get course details
    course = api.get(f'/courses/{course_id}')
    
    # Get course enrollments
    status = request.args.get('status', 'active')
    params = {'status': status} if status != 'all' else {}
    response = api.get(f'/enrollments/course/{course_id}', params=params)
    enrollments = response.get('items', [])
    
    return render_template('enrollments/course.html',
                         course=course,
                         enrollments=enrollments,
                         status=status)


@enrollments_bp.route('/enroll', methods=['POST'])
@handle_api_error
def enroll():
    """Process enrollment request"""
    form = EnrollmentForm()
    
    if form.validate_on_submit():
        api = get_api_client()
        
        try:
            # Create enrollment
            enrollment_data = {
                'student_id': int(form.student_id.data),
                'course_id': form.course_id.data
            }
            
            enrollment = api.post('/enrollments', json=enrollment_data)
            
            # Get course details for success message
            course = api.get(f'/courses/{enrollment["course_id"]}')
            flash(f'Successfully enrolled in {course["name"]}!', 'success')
            
        except APIError as e:
            if 'already enrolled' in str(e):
                flash('You are already enrolled in this course.', 'warning')
            elif 'full' in str(e):
                flash('This course is full.', 'error')
            else:
                flash(f'Enrollment failed: {e.message}', 'error')
        
        return redirect(url_for('enrollments.student_enrollments', 
                              student_id=form.student_id.data))
    
    flash('Invalid enrollment request.', 'error')
    return redirect(request.referrer or url_for('index'))


@enrollments_bp.route('/drop', methods=['POST'])
@handle_api_error
def drop():
    """Process course drop request"""
    form = DropCourseForm()
    
    if form.validate_on_submit():
        api = get_api_client()
        
        try:
            # Get enrollment details first
            enrollment_id = int(form.enrollment_id.data)
            enrollment = api.get(f'/enrollments/{enrollment_id}')
            
            # Update enrollment status to 'dropped'
            api.put(f'/enrollments/{enrollment_id}', json={'status': 'dropped'})
            
            # Get course details for success message
            course = api.get(f'/courses/{enrollment["course_id"]}')
            flash(f'Successfully dropped {course["name"]}.', 'success')
            
            return redirect(url_for('enrollments.student_enrollments', 
                                  student_id=enrollment['student_id']))
            
        except APIError as e:
            flash(f'Failed to drop course: {e.message}', 'error')
    
    flash('Invalid drop request.', 'error')
    return redirect(request.referrer or url_for('index'))


@enrollments_bp.route('/complete/<int:enrollment_id>', methods=['POST'])
@handle_api_error
def complete(enrollment_id):
    """Mark enrollment as completed"""
    api = get_api_client()
    
    try:
        # Update enrollment status to 'completed'
        enrollment = api.put(f'/enrollments/{enrollment_id}', json={'status': 'completed'})
        
        # Get course details for success message
        course = api.get(f'/courses/{enrollment["course_id"]}')
        flash(f'Marked {course["name"]} as completed.', 'success')
        
    except APIError as e:
        flash(f'Failed to update enrollment: {e.message}', 'error')
    
    return redirect(request.referrer or url_for('enrollments.index'))


@enrollments_bp.route('/delete/<int:enrollment_id>', methods=['POST'])
@handle_api_error
def delete(enrollment_id):
    """Delete enrollment record (admin only)"""
    api = get_api_client()
    
    try:
        # Delete enrollment
        api.delete(f'/enrollments/{enrollment_id}')
        flash('Enrollment record deleted successfully.', 'success')
        
    except APIError as e:
        flash(f'Failed to delete enrollment: {e.message}', 'error')
    
    return redirect(request.referrer or url_for('enrollments.index'))