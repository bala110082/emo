from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    """User model"""
    
    def __init__(self, name, email, password, age=None, sex=None):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.age = age
        self.sex = sex
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'name': self.name,
            'email': self.email,
            'password': self.password_hash,
            'age': self.age,
            'sex': self.sex,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def check_password(self, password):
        """Check if password matches"""
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def from_dict(data):
        """Create User from dictionary"""
        user = User.__new__(User)
        user.name = data.get('name')
        user.email = data.get('email')
        user.password_hash = data.get('password')
        user.age = data.get('age')
        user.sex = data.get('sex')
        user.created_at = data.get('created_at', datetime.now().isoformat())
        user.updated_at = data.get('updated_at', datetime.now().isoformat())
        return user

class EmotionRecord:
    """Emotion detection record"""
    
    def __init__(self, user_email, emotion, confidence, image_url=None):
        self.user_email = user_email
        self.emotion = emotion
        self.confidence = confidence
        self.image_url = image_url
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'user_email': self.user_email,
            'emotion': self.emotion,
            'confidence': self.confidence,
            'image_url': self.image_url,
            'timestamp': self.timestamp
        }

class MusicRecommendation:
    """Music recommendation record"""
    
    def __init__(self, user_email, emotion, tracks):
        self.user_email = user_email
        self.emotion = emotion
        self.tracks = tracks
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'user_email': self.user_email,
            'emotion': self.emotion,
            'tracks': self.tracks,
            'timestamp': self.timestamp
        }

class VideoAnalysis:
    """Video analysis record"""
    
    def __init__(self, user_email, video_url, dominant_emotion, emotion_timeline):
        self.user_email = user_email
        self.video_url = video_url
        self.dominant_emotion = dominant_emotion
        self.emotion_timeline = emotion_timeline
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'user_email': self.user_email,
            'video_url': self.video_url,
            'dominant_emotion': self.dominant_emotion,
            'emotion_timeline': self.emotion_timeline,
            'timestamp': self.timestamp
        }