import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your_secret_key_change_in_production')
    DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
    
    # Upload settings
    UPLOAD_FOLDER = 'static/uploads'
    GENERATED_FOLDER = 'static/generated'
    TEMP_FOLDER = 'static/temp'
    MAX_CONTENT_LENGTH = 60 * 1024 * 1024 
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'}
    
    # Model paths
    EMOTION_MODEL_PATH = os.getenv('EMOTION_MODEL_PATH', 'models/best_emotion_model.pth')
    MODEL_INFO_PATH = os.getenv('MODEL_INFO_PATH', 'models/model_info.json')
    
    # Spotify API
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID', '9959a1d8eb1b4f378da63ad9b59335d1')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET', '054e13dc8da540338247c00a933a20ac')
    
    # Google Gemini API
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'AIzaSyD6Z1B4At-908dalV2ohCssF9t7RIPp3NU')
    
    # Image processing
    IMG_SIZE = 224
    
    # Database
    DATABASE_PATH = 'database/users.json'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}