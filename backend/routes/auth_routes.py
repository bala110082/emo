from flask import Blueprint, request, jsonify, session
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

auth_bp = Blueprint('auth', __name__)

def load_users():
    """Load users from JSON file"""
    if os.path.exists(Config.DATABASE_PATH):
        with open(Config.DATABASE_PATH, 'r') as f:
            data = json.load(f)
            return data.get('users', [])
    return []

def save_users(users):
    """Save users to JSON file"""
    os.makedirs(os.path.dirname(Config.DATABASE_PATH), exist_ok=True)
    with open(Config.DATABASE_PATH, 'w') as f:
        json.dump({'users': users}, f, indent=4)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    
    Request:
        {
            "name": "User Name",
            "email": "user@example.com",
            "password": "password123",
            "age": 25 (optional),
            "sex": "Male/Female/Other" (optional)
        }
    
    Response:
        {
            "message": "User registered successfully",
            "user": {
                "name": "User Name",
                "email": "user@example.com"
            }
        }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['name', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        name = data['name']
        email = data['email']
        password = data['password']
        age = data.get('age', None)
        sex = data.get('sex', None)
        
        # Load existing users
        users = load_users()
        
        # Check if email already exists
        if any(user['email'] == email for user in users):
            return jsonify({'error': 'Email already registered'}), 400
        
        # Hash password
        password_hash = generate_password_hash(password)
        
        # Create new user
        new_user = {
            'name': name,
            'email': email,
            'password': password_hash,
            'age': age,
            'sex': sex
        }
        
        users.append(new_user)
        save_users(users)
        
        # Store in session
        session['user_email'] = email
        session['user_name'] = name
        
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'name': name,
                'email': email,
                'age': age,
                'sex': sex
            }
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user
    
    Request:
        {
            "email": "user@example.com",
            "password": "password123"
        }
    
    Response:
        {
            "message": "Login successful",
            "user": {
                "name": "User Name",
                "email": "user@example.com"
            }
        }
    """
    try:
        data = request.json
        
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password are required'}), 400
        
        email = data['email']
        password = data['password']
        
        # Load users
        users = load_users()
        
        # Find user
        user = next((u for u in users if u['email'] == email), None)
        
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check password
        if not check_password_hash(user['password'], password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Store in session
        session['user_email'] = email
        session['user_name'] = user['name']
        
        return jsonify({
            'message': 'Login successful',
            'user': {
                'name': user['name'],
                'email': user['email'],
                'age': user.get('age'),
                'sex': user.get('sex')
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    Logout user
    
    Response:
        {
            "message": "Logout successful"
        }
    """
    try:
        session.clear()
        return jsonify({'message': 'Logout successful'}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """
    Get current user profile
    
    Response:
        {
            "user": {
                "name": "User Name",
                "email": "user@example.com"
            }
        }
    """
    try:
        if 'user_email' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        email = session['user_email']
        
        # Load users
        users = load_users()
        
        # Find user
        user = next((u for u in users if u['email'] == email), None)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'name': user['name'],
                'email': user['email'],
                'age': user.get('age'),
                'sex': user.get('sex')
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/check-session', methods=['GET'])
def check_session():
    """
    Check if user is logged in
    
    Response:
        {
            "logged_in": true/false,
            "user": {...} (if logged in)
        }
    """
    try:
        if 'user_email' in session:
            return jsonify({
                'logged_in': True,
                'user': {
                    'name': session.get('user_name'),
                    'email': session.get('user_email')
                }
            }), 200
        else:
            return jsonify({
                'logged_in': False
            }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500