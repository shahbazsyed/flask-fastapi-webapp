"""
Authentication blueprint for Flask frontend
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from api_client import get_api_client, handle_api_error, APIError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
@handle_api_error
def login():
    """Login page and handler"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please provide both username and password', 'error')
            return render_template('auth/login.html')
        
        client = get_api_client()
        success, response = client.login(username, password)
        
        if success:
            flash('Successfully logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash(response.get('error', 'Login failed'), 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    """Logout handler"""
    client = get_api_client()
    client.logout()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
@handle_api_error
def register():
    """Registration page and handler"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Basic validation
        if not all([username, email, password, confirm_password]):
            flash('All fields are required', 'error')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('auth/register.html')
        
        # Call API to register
        client = get_api_client()
        try:
            response = client.post('/auth/register', json={
                'username': username,
                'email': email,
                'password': password
            })
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
            
        except APIError as e:
            flash(e.message, 'error')
    
    return render_template('auth/register.html')