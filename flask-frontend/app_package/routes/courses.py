"""
Course management routes for Flask frontend
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from api_client import get_api_client, handle_api_error, APIError
import logging

logger = logging.getLogger(__name__)

courses_bp = Blueprint('courses', __name__)


# Authentication decorator removed - no longer needed


@courses_bp.route('/')
@handle_api_error
def list_courses():
    """List all courses with search functionality"""
    client = get_api_client()
    
    # Get search parameters
    search_query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Build API parameters
    params = {
        'skip': (page - 1) * per_page,
        'limit': per_page
    }
    
    if search_query:
        params['search'] = search_query
    
    try:
        # Get courses from API
        response = client.get('/courses', params=params)
        
        # Extract data from paginated response
        courses = response.get('items', [])
        total = response.get('total', 0)
        
        # Calculate pagination
        total_pages = (total + per_page - 1) // per_page if per_page > 0 else 0
        
        return render_template('courses/list.html',
                             courses=courses,
                             search_query=search_query,
                             page=page,
                             per_page=per_page,
                             total=total,
                             total_pages=total_pages)
    except APIError as e:
        flash(f'Error loading courses: {e.message}', 'error')
        return render_template('courses/list.html', courses=[], total=0)


@courses_bp.route('/new', methods=['GET', 'POST'])
@handle_api_error
def create_course():
    """Create a new course"""
    if request.method == 'POST':
        # Get form data
        code = request.form.get('code', '').strip()
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        credits = request.form.get('credits', type=int)
        
        # Validate required fields
        if not all([code, name, credits]):
            flash('Course code, name, and credits are required', 'error')
            return render_template('courses/create.html')
        
        # Create course via API
        client = get_api_client()
        try:
            course_data = {
                'course_code': code,
                'name': name,
                'description': description,
                'credits': credits,
                'max_students': 30  # Default max students
            }
            
            response = client.post('/courses', json=course_data)
            flash(f'Course "{name}" created successfully!', 'success')
            return redirect(url_for('courses.view_course', course_id=response['id']))
            
        except APIError as e:
            flash(f'Error creating course: {e.message}', 'error')
    
    return render_template('courses/create.html')


@courses_bp.route('/<int:course_id>')
@handle_api_error
def view_course(course_id):
    """View course details including enrolled students"""
    client = get_api_client()
    
    try:
        # Get course details
        course = client.get(f'/courses/{course_id}')
        
        # Get enrolled students for this course
        enrollments_response = client.get(f'/enrollments/course/{course_id}')
        enrollments = enrollments_response.get('items', [])
        
        # Check if current user is enrolled - removed (no auth)
        is_enrolled = False
        
        return render_template('courses/detail.html',
                             course=course,
                             enrollments=enrollments,
                             is_enrolled=is_enrolled)
                             
    except APIError as e:
        if e.status_code == 404:
            flash('Course not found', 'error')
            return redirect(url_for('courses.list_courses'))
        flash(f'Error loading course: {e.message}', 'error')
        return redirect(url_for('courses.list_courses'))


@courses_bp.route('/<int:course_id>/edit', methods=['GET', 'POST'])
@handle_api_error
def edit_course(course_id):
    """Edit course details"""
    client = get_api_client()
    
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        credits = request.form.get('credits', type=int)
        
        # Validate required fields
        if not all([name, credits]):
            flash('Course name and credits are required', 'error')
            return redirect(request.url)
        
        try:
            # Update course via API
            update_data = {
                'name': name,
                'description': description,
                'credits': credits
            }
            
            response = client.put(f'/courses/{course_id}', json=update_data)
            flash('Course updated successfully!', 'success')
            return redirect(url_for('courses.view_course', course_id=course_id))
            
        except APIError as e:
            flash(f'Error updating course: {e.message}', 'error')
    
    # GET request - load course data
    try:
        course = client.get(f'/courses/{course_id}')
        return render_template('courses/edit.html', course=course)
        
    except APIError as e:
        if e.status_code == 404:
            flash('Course not found', 'error')
            return redirect(url_for('courses.list_courses'))
        flash(f'Error loading course: {e.message}', 'error')
        return redirect(url_for('courses.list_courses'))


@courses_bp.route('/<int:course_id>/delete', methods=['POST'])
@handle_api_error
def delete_course(course_id):
    """Delete a course"""
    client = get_api_client()
    
    try:
        client.delete(f'/courses/{course_id}')
        flash('Course deleted successfully!', 'success')
        
    except APIError as e:
        if e.status_code == 404:
            flash('Course not found', 'error')
        else:
            flash(f'Error deleting course: {e.message}', 'error')
    
    return redirect(url_for('courses.list_courses'))


@courses_bp.route('/<int:course_id>/enroll', methods=['POST'])
@handle_api_error
def enroll_course(course_id):
    """Enroll in a course - simplified without auth"""
    # For demo purposes, we'll need to get student_id from request
    student_id = request.form.get('student_id')
    
    if not student_id:
        flash('Student ID is required for enrollment', 'error')
        return redirect(url_for('courses.view_course', course_id=course_id))
    
    client = get_api_client()
    
    try:
        # Create enrollment
        enrollment_data = {
            'student_id': int(student_id),
            'course_id': course_id
        }
        
        client.post('/enrollments', json=enrollment_data)
        flash('Successfully enrolled in course!', 'success')
        
    except APIError as e:
        if 'already enrolled' in e.message.lower():
            flash('You are already enrolled in this course', 'info')
        else:
            flash(f'Error enrolling in course: {e.message}', 'error')
    
    return redirect(url_for('courses.view_course', course_id=course_id))


@courses_bp.route('/<int:course_id>/unenroll', methods=['POST'])
@handle_api_error
def unenroll_course(course_id):
    """Unenroll from a course - simplified without auth"""
    # For demo purposes, we'll need to get student_id from request
    student_id = request.form.get('student_id')
    
    if not student_id:
        flash('Student ID is required for unenrollment', 'error')
        return redirect(url_for('courses.view_course', course_id=course_id))
    
    client = get_api_client()
    
    try:
        # Find enrollment ID
        enrollments_response = client.get(f'/enrollments/student/{student_id}')
        enrollments = enrollments_response.get('items', [])
        enrollment = next((e for e in enrollments if e['course_id'] == course_id), None)
        
        if enrollment:
            client.delete(f'/enrollments/{enrollment["id"]}')
            flash('Successfully unenrolled from course!', 'success')
        else:
            flash('You are not enrolled in this course', 'info')
        
    except APIError as e:
        flash(f'Error unenrolling from course: {e.message}', 'error')
    
    return redirect(url_for('courses.view_course', course_id=course_id))


# Alias for compatibility with existing navigation
index = list_courses