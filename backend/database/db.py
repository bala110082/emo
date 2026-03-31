import json
import os
from config import Config

class Database:
    """Simple JSON-based database for user management"""
    
    def __init__(self, db_path=None):
        self.db_path = db_path or Config.DATABASE_PATH
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Create database file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        if not os.path.exists(self.db_path):
            self._write_data({'users': []})
    
    def _read_data(self):
        """Read data from JSON file"""
        try:
            with open(self.db_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading database: {str(e)}")
            return {'users': []}
    
    def _write_data(self, data):
        """Write data to JSON file"""
        try:
            with open(self.db_path, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error writing database: {str(e)}")
            return False
    
    def get_all_users(self):
        """Get all users"""
        data = self._read_data()
        return data.get('users', [])
    
    def get_user_by_email(self, email):
        """Get user by email"""
        users = self.get_all_users()
        for user in users:
            if user.get('email') == email:
                return user
        return None
    
    def create_user(self, user_data):
        """Create new user"""
        data = self._read_data()
        users = data.get('users', [])
        
        # Check if email already exists
        if any(u.get('email') == user_data.get('email') for u in users):
            return False, "Email already exists"
        
        users.append(user_data)
        data['users'] = users
        
        if self._write_data(data):
            return True, "User created successfully"
        return False, "Failed to create user"
    
    def update_user(self, email, update_data):
        """Update user data"""
        data = self._read_data()
        users = data.get('users', [])
        
        for i, user in enumerate(users):
            if user.get('email') == email:
                users[i].update(update_data)
                data['users'] = users
                
                if self._write_data(data):
                    return True, "User updated successfully"
                return False, "Failed to update user"
        
        return False, "User not found"
    
    def delete_user(self, email):
        """Delete user"""
        data = self._read_data()
        users = data.get('users', [])
        
        users = [u for u in users if u.get('email') != email]
        data['users'] = users
        
        if self._write_data(data):
            return True, "User deleted successfully"
        return False, "Failed to delete user"
    
    def user_exists(self, email):
        """Check if user exists"""
        return self.get_user_by_email(email) is not None

# Singleton instance
db = Database()