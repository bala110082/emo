import os
import re
from werkzeug.utils import secure_filename

# Allowed file extensions
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm', 'flv'}
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'ogg', 'flac', 'm4a'}

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def allowed_image(filename):
    """Check if image file is allowed"""
    return allowed_file(filename, ALLOWED_IMAGE_EXTENSIONS)

def allowed_video(filename):
    """Check if video file is allowed"""
    return allowed_file(filename, ALLOWED_VIDEO_EXTENSIONS)

def allowed_audio(filename):
    """Check if audio file is allowed"""
    return allowed_file(filename, ALLOWED_AUDIO_EXTENSIONS)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """
    Validate password strength
    
    Requirements:
    - At least 6 characters
    
    Returns:
        tuple: (is_valid, message)
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    return True, "Password is valid"

def validate_username(username):
    """
    Validate username
    
    Requirements:
    - 3-20 characters
    - Alphanumeric and underscores only
    
    Returns:
        tuple: (is_valid, message)
    """
    if len(username) < 3 or len(username) > 20:
        return False, "Username must be 3-20 characters"
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, "Username is valid"

def validate_emotion(emotion):
    """Validate emotion string"""
    valid_emotions = [
        'happy', 'sad', 'angry', 'fear', 'disgust', 'surprise', 'neutral',
        'Happy', 'Sad', 'Angry', 'Fear', 'Disgust', 'Surprise', 'Neutral'
    ]
    return emotion in valid_emotions

def validate_sentiment(sentiment):
    """Validate sentiment string"""
    valid_sentiments = ['POS', 'NEG', 'NEU', 'pos', 'neg', 'neu']
    return sentiment in valid_sentiments

def validate_limit(limit, min_val=1, max_val=50):
    """Validate limit parameter"""
    try:
        limit = int(limit)
        return min_val <= limit <= max_val
    except:
        return False

def validate_duration(duration, min_val=5, max_val=120):
    """Validate duration parameter"""
    try:
        duration = int(duration)
        return min_val <= duration <= max_val
    except:
        return False

def validate_bpm(bpm, min_val=40, max_val=200):
    """Validate BPM parameter"""
    try:
        bpm = int(bpm)
        return min_val <= bpm <= max_val
    except:
        return False

def validate_temperature(temperature, min_val=0.0, max_val=2.0):
    """Validate temperature parameter"""
    try:
        temperature = float(temperature)
        return min_val <= temperature <= max_val
    except:
        return False

def validate_fps(fps, min_val=0.5, max_val=30):
    """Validate FPS parameter"""
    try:
        fps = float(fps)
        return min_val <= fps <= max_val
    except:
        return False

def validate_file_size(file, max_size_mb=16):
    """Validate file size"""
    try:
        file.seek(0, os.SEEK_END)
        size = file.tell()
        file.seek(0)
        
        max_size_bytes = max_size_mb * 1024 * 1024
        return size <= max_size_bytes
    except:
        return False

def sanitize_filename(filename):
    """Sanitize filename"""
    return secure_filename(filename)

def validate_json_data(data, required_fields):
    """
    Validate JSON data has required fields
    
    Args:
        data: dict
        required_fields: list of required field names
    
    Returns:
        tuple: (is_valid, missing_fields)
    """
    if not data:
        return False, required_fields
    
    missing = [field for field in required_fields if field not in data]
    
    return len(missing) == 0, missing

def validate_base64_image(base64_string):
    """Validate base64 image string"""
    try:
        # Check if it has data URL prefix
        if base64_string.startswith('data:image'):
            if ',' not in base64_string:
                return False
            base64_string = base64_string.split(',')[1]
        
        # Check if it's valid base64
        import base64
        base64.b64decode(base64_string)
        return True
    except:
        return False

def validate_path(path, must_exist=True):
    """Validate file path"""
    if must_exist:
        return os.path.exists(path)
    else:
        # Check if parent directory exists
        parent = os.path.dirname(path)
        return os.path.exists(parent) if parent else True