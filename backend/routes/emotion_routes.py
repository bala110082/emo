# # from flask import Blueprint, request, jsonify
# # from werkzeug.utils import secure_filename
# # import os
# # import base64
# # from io import BytesIO
# # from PIL import Image
# # from services.emotion_service import emotion_service
# # from config import Config

# # emotion_bp = Blueprint('emotion', __name__)

# # def allowed_file(filename):
# #     return '.' in filename and \
# #            filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# # @emotion_bp.route('/detect-image', methods=['POST'])
# # def detect_emotion_from_image():
# #     """
# #     Detect emotion from uploaded image
    
# #     Request:
# #         - file: image file (multipart/form-data)
# #         OR
# #         - image: base64 encoded image (JSON)
    
# #     Response:
# #         {
# #             "emotions": {...},
# #             "top_emotion": "Happy",
# #             "confidence": 85.3,
# #             "face_detected": true,
# #             "image_url": "/static/uploads/..."
# #         }
# #     """
# #     try:
# #         # Check if image is uploaded as file
# #         if 'file' in request.files:
# #             file = request.files['file']
            
# #             if file.filename == '':
# #                 return jsonify({'error': 'No file selected'}), 400
            
# #             if not allowed_file(file.filename):
# #                 return jsonify({'error': 'Invalid file type'}), 400
            
# #             # Save file
# #             filename = secure_filename(file.filename)
# #             filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
# #             file.save(filepath)
        
# #         # Check if image is sent as base64
# #         elif request.is_json and 'image' in request.json:
# #             image_data = request.json['image']
            
# #             # Remove data URL prefix if present
# #             if ',' in image_data:
# #                 image_data = image_data.split(',')[1]
            
# #             # Decode and save
# #             image_bytes = base64.b64decode(image_data)
# #             image = Image.open(BytesIO(image_bytes))
            
# #             filename = 'uploaded_image.jpg'
# #             filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
# #             image.save(filepath)
        
# #         else:
# #             return jsonify({'error': 'No image provided'}), 400
        
# #         # Detect emotion (use custom model for image upload)
# #         result = emotion_service.detect_from_image(filepath, use_deepface=False)
        
# #         if 'error' in result:
# #             return jsonify(result), 400
        
# #         # Add image URL to response
# #         result['image_url'] = f'/static/uploads/{filename}'
        
# #         return jsonify(result), 200
    
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# # @emotion_bp.route('/detect-live', methods=['POST'])
# # def detect_emotion_live():
# #     """
# #     Detect emotion from webcam frame (real-time)
    
# #     Request:
# #         {
# #             "image": "base64_encoded_frame"
# #         }
    
# #     Response:
# #         {
# #             "emotions": {...},
# #             "top_emotion": "Happy",
# #             "confidence": 85.3,
# #             "face_detected": true
# #         }
# #     """
# #     try:
# #         if not request.is_json:
# #             return jsonify({'error': 'Content-Type must be application/json'}), 400
        
# #         data = request.json
        
# #         if 'image' not in data:
# #             return jsonify({'error': 'No image data provided'}), 400
        
# #         # Decode base64 image
# #         image_data = data['image']
# #         if ',' in image_data:
# #             image_data = image_data.split(',')[1]
        
# #         image_bytes = base64.b64decode(image_data)
# #         image = Image.open(BytesIO(image_bytes))
        
# #         # Save temporarily
# #         filename = 'webcam_frame.jpg'
# #         filepath = os.path.join(Config.TEMP_FOLDER, filename)
# #         image.save(filepath)
        
# #         # Detect emotion (use DeepFace for live detection - faster)
# #         result = emotion_service.detect_from_image(filepath, use_deepface=True)
        
# #         if 'error' in result:
# #             return jsonify(result), 400
        
# #         return jsonify(result), 200
    
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# # @emotion_bp.route('/emotions-list', methods=['GET'])
# # def get_emotions_list():
# #     """
# #     Get list of all supported emotions
    
# #     Response:
# #         {
# #             "emotions": ["Happy", "Sad", "Angry", ...]
# #         }
# #     """
# #     return jsonify({
# #         'emotions': emotion_service.emotion_classes
# #     }), 200


# from flask import Blueprint, request, jsonify
# from werkzeug.utils import secure_filename
# import os
# import base64
# from io import BytesIO
# from PIL import Image
# from services.emotion_service import emotion_service
# from services.gemini_service import gemini_service
# from config import Config
# import time

# emotion_bp = Blueprint('emotion', __name__)

# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# @emotion_bp.route('/detect-image', methods=['POST'])
# def detect_emotion_from_image():
#     """
#     Detect emotion from uploaded image
    
#     Request:
#         - file: image file (multipart/form-data)
#         OR
#         - image: base64 encoded image (JSON)
#         Optional:
#         - generate_bgm: bool (default False) - whether to generate BGM
    
#     Response:
#         {
#             "emotions": {...},
#             "top_emotion": "Happy",
#             "confidence": 85.3,
#             "face_detected": true,
#             "image_url": "/static/uploads/...",
#             "bgm": {...}  // if generate_bgm=true
#         }
#     """
#     try:
#         # Check if image is uploaded as file
#         if 'file' in request.files:
#             file = request.files['file']
            
#             if file.filename == '':
#                 return jsonify({'error': 'No file selected'}), 400
            
#             if not allowed_file(file.filename):
#                 return jsonify({'error': 'Invalid file type'}), 400
            
#             # Save file
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
#             file.save(filepath)
        
#         # Check if image is sent as base64
#         elif request.is_json and 'image' in request.json:
#             image_data = request.json['image']
            
#             # Remove data URL prefix if present
#             if ',' in image_data:
#                 image_data = image_data.split(',')[1]
            
#             # Decode and save
#             image_bytes = base64.b64decode(image_data)
#             image = Image.open(BytesIO(image_bytes))
            
#             filename = 'uploaded_image.jpg'
#             filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
#             image.save(filepath)
        
#         else:
#             return jsonify({'error': 'No image provided'}), 400
        
#         # Detect emotion (use custom model for image upload)
#         result = emotion_service.detect_from_image(filepath, use_deepface=False)
        
#         if 'error' in result:
#             return jsonify(result), 400
        
#         # Add image URL to response
#         result['image_url'] = f'/static/uploads/{filename}'
        
#         # Check if BGM generation is requested
#         generate_bgm = request.form.get('generate_bgm', 'false').lower() == 'true' if 'file' in request.files else request.json.get('generate_bgm', False)
        
#         if generate_bgm:
#             emotion = result['top_emotion']
#             print(f"🎵 Generating BGM for emotion: {emotion}")
            
#             # Generate 20-second BGM
#             bgm_result = gemini_service.generate_bgm_sync(emotion=emotion, duration=20)
            
#             if 'error' not in bgm_result and bgm_result.get('audio_data'):
#                 # Save BGM file
#                 bgm_filename = f"bgm_{emotion.lower()}_{int(time.time())}.wav"
#                 bgm_filepath = os.path.join(Config.GENERATED_FOLDER, bgm_filename)
                
#                 if gemini_service.save_bgm_to_file(bgm_result['audio_data'], bgm_filepath):
#                     result['bgm'] = {
#                         'audio_url': f'/static/generated/{bgm_filename}',
#                         'emotion': emotion,
#                         'duration': bgm_result.get('duration', 20),
#                         'bpm': bgm_result.get('bpm'),
#                         'file_size_mb': bgm_result.get('file_size_mb')
#                     }
#                     print(f"✅ BGM saved: {bgm_filename}")
#                 else:
#                     result['bgm_error'] = 'Failed to save BGM file'
#             else:
#                 result['bgm_error'] = bgm_result.get('error', 'BGM generation failed')
        
#         return jsonify(result), 200
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @emotion_bp.route('/detect-live', methods=['POST'])
# def detect_emotion_live():
#     """
#     Detect emotion from webcam frame (real-time)
    
#     Request:
#         {
#             "image": "base64_encoded_frame"
#         }
    
#     Response:
#         {
#             "emotions": {...},
#             "top_emotion": "Happy",
#             "confidence": 85.3,
#             "face_detected": true
#         }
#     """
#     try:
#         if not request.is_json:
#             return jsonify({'error': 'Content-Type must be application/json'}), 400
        
#         data = request.json
        
#         if 'image' not in data:
#             return jsonify({'error': 'No image data provided'}), 400
        
#         # Decode base64 image
#         image_data = data['image']
#         if ',' in image_data:
#             image_data = image_data.split(',')[1]
        
#         image_bytes = base64.b64decode(image_data)
#         image = Image.open(BytesIO(image_bytes))
        
#         # Save temporarily
#         filename = 'webcam_frame.jpg'
#         filepath = os.path.join(Config.TEMP_FOLDER, filename)
#         image.save(filepath)
        
#         # Detect emotion (use DeepFace for live detection - faster)
#         result = emotion_service.detect_from_image(filepath, use_deepface=True)
        
#         if 'error' in result:
#             return jsonify(result), 400
        
#         return jsonify(result), 200
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @emotion_bp.route('/generate-bgm-for-emotion', methods=['POST'])
# def generate_bgm_for_detected_emotion():
#     """
#     Generate BGM for a specific emotion (used by webcam after session ends)
    
#     Request:
#         {
#             "emotion": "Happy",
#             "duration": 20  // optional, default 20
#         }
    
#     Response:
#         {
#             "audio_url": "/static/generated/bgm_happy_xxx.wav",
#             "emotion": "Happy",
#             "duration": 20,
#             "bpm": 120,
#             "file_size_mb": 2.5
#         }
#     """
#     try:
#         data = request.json
        
#         if not data or 'emotion' not in data:
#             return jsonify({'error': 'Emotion is required'}), 400
        
#         emotion = data['emotion']
#         duration = data.get('duration', 20)
        
#         print(f"🎵 Generating BGM for webcam session: {emotion}")
        
#         # Generate BGM
#         bgm_result = gemini_service.generate_bgm_sync(emotion=emotion, duration=duration)
        
#         if 'error' in bgm_result:
#             return jsonify(bgm_result), 500
        
#         if not bgm_result.get('audio_data'):
#             return jsonify({'error': 'No audio data generated'}), 500
        
#         # Save BGM file
#         bgm_filename = f"bgm_webcam_{emotion.lower()}_{int(time.time())}.wav"
#         bgm_filepath = os.path.join(Config.GENERATED_FOLDER, bgm_filename)
        
#         if gemini_service.save_bgm_to_file(bgm_result['audio_data'], bgm_filepath):
#             return jsonify({
#                 'success': True,
#                 'audio_url': f'/static/generated/{bgm_filename}',
#                 'emotion': emotion,
#                 'duration': bgm_result.get('duration', duration),
#                 'bpm': bgm_result.get('bpm'),
#                 'file_size_mb': bgm_result.get('file_size_mb'),
#                 'prompt': bgm_result.get('prompt')
#             }), 200
#         else:
#             return jsonify({'error': 'Failed to save BGM file'}), 500
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @emotion_bp.route('/emotions-list', methods=['GET'])
# def get_emotions_list():
#     """
#     Get list of all supported emotions
    
#     Response:
#         {
#             "emotions": ["Happy", "Sad", "Angry", ...]
#         }
#     """
#     return jsonify({
#         'emotions': emotion_service.emotion_classes
#     }), 200

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import base64
from io import BytesIO
from PIL import Image
from services.emotion_service import emotion_service
from services.gemini_service import gemini_service
from config import Config
import time

emotion_bp = Blueprint('emotion', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@emotion_bp.route('/detect-image', methods=['POST'])
def detect_emotion_from_image():
    """
    Detect emotion from uploaded image
    
    Request:
        - file: image file (multipart/form-data)
        OR
        - image: base64 encoded image (JSON)
        Optional:
        - generate_bgm: bool (default False) - whether to generate BGM
    
    Response:
        {
            "emotions": {...},
            "top_emotion": "Happy",
            "confidence": 85.3,
            "face_detected": true,
            "image_url": "/static/uploads/...",
            "bgm": {...}  // if generate_bgm=true
        }
    """
    try:
        # Check if image is uploaded as file
        if 'file' in request.files:
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if not allowed_file(file.filename):
                return jsonify({'error': 'Invalid file type'}), 400
            
            # Save file
            filename = secure_filename(file.filename)
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(filepath)
        
        # Check if image is sent as base64
        elif request.is_json and 'image' in request.json:
            image_data = request.json['image']
            
            # Remove data URL prefix if present
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decode and save
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))
            
            filename = 'uploaded_image.jpg'
            filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
            image.save(filepath)
        
        else:
            return jsonify({'error': 'No image provided'}), 400
        
        # Detect emotion (use custom model for image upload)
        result = emotion_service.detect_from_image(filepath, use_deepface=False)
        
        if 'error' in result:
            return jsonify(result), 400
        
        # Add image URL to response
        result['image_url'] = f'/static/uploads/{filename}'
        
        # Check if BGM generation is requested
        generate_bgm = request.form.get('generate_bgm', 'false').lower() == 'true' if 'file' in request.files else request.json.get('generate_bgm', False)
        
        if generate_bgm:
            emotion = result['top_emotion']
            print(f"🎵 Generating BGM for emotion: {emotion}")
            
            # Generate 20-second BGM
            bgm_result = gemini_service.generate_bgm_sync(emotion=emotion, duration=20)
            
            if 'error' not in bgm_result and bgm_result.get('audio_data'):
                # Save BGM file
                bgm_filename = f"bgm_{emotion.lower()}_{int(time.time())}.wav"
                bgm_filepath = os.path.join(Config.GENERATED_FOLDER, bgm_filename)
                
                if gemini_service.save_bgm_to_file(bgm_result['audio_data'], bgm_filepath):
                    result['bgm'] = {
                        'audio_url': f'/static/generated/{bgm_filename}',
                        'emotion': emotion,
                        'duration': bgm_result.get('duration', 20),
                        'bpm': bgm_result.get('bpm'),
                        'file_size_mb': bgm_result.get('file_size_mb')
                    }
                    print(f"✅ BGM saved: {bgm_filename}")
                    
                    # AUTO-PLAY in local media player
                    gemini_service.play_audio_file(bgm_filepath)
                else:
                    result['bgm_error'] = 'Failed to save BGM file'
            else:
                result['bgm_error'] = bgm_result.get('error', 'BGM generation failed')
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@emotion_bp.route('/detect-live', methods=['POST'])
def detect_emotion_live():
    """
    Detect emotion from webcam frame (real-time)
    
    Request:
        {
            "image": "base64_encoded_frame"
        }
    
    Response:
        {
            "emotions": {...},
            "top_emotion": "Happy",
            "confidence": 85.3,
            "face_detected": true
        }
    """
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.json
        
        if 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Decode base64 image
        image_data = data['image']
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        
        # Save temporarily
        filename = 'webcam_frame.jpg'
        filepath = os.path.join(Config.TEMP_FOLDER, filename)
        image.save(filepath)
        
        # Detect emotion (use DeepFace for live detection - faster)
        result = emotion_service.detect_from_image(filepath, use_deepface=True)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@emotion_bp.route('/generate-bgm-for-emotion', methods=['POST'])
def generate_bgm_for_detected_emotion():
    """
    Generate BGM for a specific emotion (used by webcam after session ends)
    
    Request:
        {
            "emotion": "Happy",
            "duration": 20  // optional, default 20
        }
    
    Response:
        {
            "audio_url": "/static/generated/bgm_happy_xxx.wav",
            "emotion": "Happy",
            "duration": 20,
            "bpm": 120,
            "file_size_mb": 2.5
        }
    """
    try:
        data = request.json
        
        if not data or 'emotion' not in data:
            return jsonify({'error': 'Emotion is required'}), 400
        
        emotion = data['emotion']
        duration = data.get('duration', 20)
        
        print(f"🎵 Generating BGM for webcam session: {emotion}")
        
        # Generate BGM
        bgm_result = gemini_service.generate_bgm_sync(emotion=emotion, duration=duration)
        
        if 'error' in bgm_result:
            return jsonify(bgm_result), 500
        
        if not bgm_result.get('audio_data'):
            return jsonify({'error': 'No audio data generated'}), 500
        
        # Save BGM file
        bgm_filename = f"bgm_webcam_{emotion.lower()}_{int(time.time())}.wav"
        bgm_filepath = os.path.join(Config.GENERATED_FOLDER, bgm_filename)
        
        if gemini_service.save_bgm_to_file(bgm_result['audio_data'], bgm_filepath):
            # AUTO-PLAY in local media player
            gemini_service.play_audio_file(bgm_filepath)
            
            return jsonify({
                'success': True,
                'audio_url': f'/static/generated/{bgm_filename}',
                'emotion': emotion,
                'duration': bgm_result.get('duration', duration),
                'bpm': bgm_result.get('bpm'),
                'file_size_mb': bgm_result.get('file_size_mb'),
                'prompt': bgm_result.get('prompt')
            }), 200
        else:
            return jsonify({'error': 'Failed to save BGM file'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@emotion_bp.route('/emotions-list', methods=['GET'])
def get_emotions_list():
    """
    Get list of all supported emotions
    
    Response:
        {
            "emotions": ["Happy", "Sad", "Angry", ...]
        }
    """
    return jsonify({
        'emotions': emotion_service.emotion_classes
    }), 200