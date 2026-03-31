from flask import Flask, request, jsonify, session, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_secret_key_change_in_production')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['GENERATED_FOLDER'] = 'static/generated'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024

# Enable CORS
CORS(app, supports_credentials=True)

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)
os.makedirs('static/temp', exist_ok=True)

# Import routes
from routes.auth_routes import auth_bp
from routes.emotion_routes import emotion_bp
from routes.music_routes import music_bp
from routes.video_routes import video_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(emotion_bp, url_prefix='/api/emotion')
app.register_blueprint(music_bp, url_prefix='/api/music')
app.register_blueprint(video_bp, url_prefix='/api/video')

# Serve frontend
@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/api')
def api_info():
    return jsonify({
        'message': 'EmoRhythm API - AI Adaptive Music System',
        'version': '1.0.0',
        'endpoints': {
            'auth': '/api/auth',
            'emotion': '/api/emotion',
            'music': '/api/music',
            'video': '/api/video'
        }
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)