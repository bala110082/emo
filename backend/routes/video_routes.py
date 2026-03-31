# # from flask import Blueprint, request, jsonify, send_file
# # from werkzeug.utils import secure_filename
# # import os
# # from services.video_service import video_service
# # from services.gemini_service import gemini_service
# # from config import Config
# # import base64

# # video_bp = Blueprint('video', __name__)

# # def allowed_video_file(filename):
# #     return '.' in filename and \
# #            filename.rsplit('.', 1)[1].lower() in {'mp4', 'avi', 'mov', 'mkv', 'webm'}

# # @video_bp.route('/analyze', methods=['POST'])
# # def analyze_video():
# #     """
# #     Analyze emotions in a video
    
# #     Request:
# #         - file: video file (multipart/form-data)
# #         - fps: frames per second to analyze (optional, default 1)
    
# #     Response:
# #         {
# #             "emotion_timeline": [
# #                 {
# #                     "timestamp": 1.5,
# #                     "emotion": "Happy",
# #                     "confidence": 85.3,
# #                     "all_emotions": {...}
# #                 },
# #                 ...
# #             ],
# #             "dominant_emotion": "Happy",
# #             "dominant_percentage": 65.5,
# #             "emotion_distribution": {
# #                 "Happy": 20,
# #                 "Sad": 5,
# #                 ...
# #             },
# #             "total_frames_analyzed": 30,
# #             "video_duration": 30.5
# #         }
# #     """
# #     try:
# #         # Check if video file is uploaded
# #         if 'file' not in request.files:
# #             return jsonify({'error': 'No video file provided'}), 400
        
# #         file = request.files['file']
        
# #         if file.filename == '':
# #             return jsonify({'error': 'No file selected'}), 400
        
# #         if not allowed_video_file(file.filename):
# #             return jsonify({'error': 'Invalid video file type'}), 400
        
# #         # Get FPS parameter
# #         fps = request.form.get('fps', 1)
# #         try:
# #             fps = int(fps)
# #         except:
# #             fps = 1
        
# #         # Save video file
# #         filename = secure_filename(file.filename)
# #         filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
# #         file.save(filepath)
        
# #         # Analyze video emotions
# #         result = video_service.analyze_video_emotions(filepath, fps=fps)
        
# #         if 'error' in result:
# #             return jsonify(result), 400
        
# #         result['video_filename'] = filename
        
# #         return jsonify(result), 200
    
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# # @video_bp.route('/generate-bgm', methods=['POST'])
# # def generate_bgm():
# #     """
# #     Generate background music for video based on emotions
    
# #     Request:
# #         - file: video file (multipart/form-data)
# #         OR
# #         - video_path: path to already uploaded video (JSON)
        
# #         Optional:
# #         - fps: frames per second for analysis (default 1)
    
# #     Response:
# #         {
# #             "analysis": {
# #                 "emotion_timeline": [...],
# #                 "dominant_emotion": "Happy",
# #                 ...
# #             },
# #             "bgm": {
# #                 "audio_data": "base64_encoded_audio",
# #                 "format": "audio/wav",
# #                 "duration": 30,
# #                 "emotion": "Happy",
# #                 "bpm": 120
# #             },
# #             "bgm_url": "/static/generated/bgm_filename.wav",
# #             "success": true
# #         }
# #     """
# #     try:
# #         video_path = None
        
# #         # Check if video file is uploaded
# #         if 'file' in request.files:
# #             file = request.files['file']
            
# #             if file.filename == '':
# #                 return jsonify({'error': 'No file selected'}), 400
            
# #             if not allowed_video_file(file.filename):
# #                 return jsonify({'error': 'Invalid video file type'}), 400
            
# #             # Save video file
# #             filename = secure_filename(file.filename)
# #             video_path = os.path.join(Config.UPLOAD_FOLDER, filename)
# #             file.save(video_path)
        
# #         # Check if video path is provided
# #         elif request.is_json and 'video_path' in request.json:
# #             video_path = request.json['video_path']
            
# #             if not os.path.exists(video_path):
# #                 return jsonify({'error': 'Video file not found'}), 400
        
# #         else:
# #             return jsonify({'error': 'No video file provided'}), 400
        
# #         # Generate output audio path
# #         video_basename = os.path.basename(video_path)
# #         audio_filename = f"bgm_{os.path.splitext(video_basename)[0]}.wav"
# #         audio_path = os.path.join(Config.GENERATED_FOLDER, audio_filename)
        
# #         # Generate BGM
# #         result = video_service.generate_video_bgm(video_path, output_path=audio_path)
        
# #         if not result.get('success'):
# #             return jsonify(result), 500
        
# #         # Add audio URL to response
# #         result['bgm_url'] = f'/static/generated/{audio_filename}'
        
# #         return jsonify(result), 200
    
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# # @video_bp.route('/generate-bgm-emotion', methods=['POST'])
# # def generate_bgm_for_emotion():
# #     """
# #     Generate background music for a specific emotion (no video required)
    
# #     Request:
# #         {
# #             "emotion": "Happy",
# #             "bpm": 120 (optional),
# #             "temperature": 1.0 (optional),
# #             "duration": 30 (optional, in seconds)
# #         }
    
# #     Response:
# #         {
# #             "audio_data": "base64_encoded_audio",
# #             "format": "audio/wav",
# #             "duration": 30,
# #             "emotion": "Happy",
# #             "bpm": 120
# #         }
# #     """
# #     try:
# #         data = request.json
        
# #         if not data or 'emotion' not in data:
# #             return jsonify({'error': 'Emotion is required'}), 400
        
# #         emotion = data['emotion']
# #         bpm = data.get('bpm', None)
# #         temperature = data.get('temperature', 1.0)
# #         duration = data.get('duration', 30)
        
# #         # Validate parameters
# #         if temperature < 0.0 or temperature > 2.0:
# #             temperature = 1.0
        
# #         if duration < 5 or duration > 120:
# #             duration = 30
        
# #         # Generate BGM
# #         result = gemini_service.generate_bgm_sync(
# #             emotion=emotion,
# #             bpm=bpm,
# #             temperature=temperature,
# #             duration=duration
# #         )
        
# #         if 'error' in result:
# #             return jsonify(result), 500
        
# #         # Optionally save to file
# #         save_file = data.get('save_file', False)
# #         if save_file and result.get('audio_data'):
# #             try:
# #                 audio_filename = f"bgm_{emotion.lower()}_{duration}s.wav"
# #                 audio_path = os.path.join(Config.GENERATED_FOLDER, audio_filename)
                
# #                 audio_bytes = base64.b64decode(result['audio_data'])
# #                 with open(audio_path, 'wb') as f:
# #                     f.write(audio_bytes)
                
# #                 result['audio_url'] = f'/static/generated/{audio_filename}'
# #             except Exception as e:
# #                 print(f"Error saving audio file: {str(e)}")
        
# #         return jsonify(result), 200
    
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500

# # @video_bp.route('/download-bgm/<filename>', methods=['GET'])
# # def download_bgm(filename):
# #     """
# #     Download generated BGM file
    
# #     URL: /api/video/download-bgm/<filename>
# #     """
# #     try:
# #         filepath = os.path.join(Config.GENERATED_FOLDER, filename)
        
# #         if not os.path.exists(filepath):
# #             return jsonify({'error': 'File not found'}), 404
        
# #         return send_file(filepath, as_attachment=True)
    
# #     except Exception as e:
# #         return jsonify({'error': str(e)}), 500


# from flask import Blueprint, request, jsonify, send_file
# from werkzeug.utils import secure_filename
# import os
# from services.video_service import video_service
# from services.gemini_service import gemini_service
# from config import Config
# import base64
# import time

# video_bp = Blueprint('video', __name__)

# def allowed_video_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in {'mp4', 'avi', 'mov', 'mkv', 'webm'}

# @video_bp.route('/analyze', methods=['POST'])
# def analyze_video():
#     """
#     Analyze emotions in a video
    
#     Request:
#         - file: video file (multipart/form-data)
#         - fps: frames per second to analyze (optional, default 1)
    
#     Response:
#         {
#             "emotion_timeline": [...],
#             "dominant_emotion": "Happy",
#             "dominant_percentage": 65.5,
#             "emotion_distribution": {...},
#             "total_frames_analyzed": 30,
#             "video_duration": 30.5
#         }
#     """
#     try:
#         if 'file' not in request.files:
#             return jsonify({'error': 'No video file provided'}), 400
        
#         file = request.files['file']
        
#         if file.filename == '':
#             return jsonify({'error': 'No file selected'}), 400
        
#         if not allowed_video_file(file.filename):
#             return jsonify({'error': 'Invalid video file type'}), 400
        
#         fps = request.form.get('fps', 1)
#         try:
#             fps = int(fps)
#         except:
#             fps = 1
        
#         # Save video file
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
#         file.save(filepath)
        
#         # Analyze video emotions
#         result = video_service.analyze_video_emotions(filepath, fps=fps)
        
#         if 'error' in result:
#             return jsonify(result), 400
        
#         result['video_filename'] = filename
        
#         return jsonify(result), 200
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @video_bp.route('/generate-bgm', methods=['POST'])
# def generate_bgm():
#     """
#     Generate 20-second background music for video based on emotions
    
#     Request:
#         - file: video file (multipart/form-data)
#         OR
#         - video_path: path to already uploaded video (JSON)
        
#         Optional:
#         - fps: frames per second for analysis (default 1)
#         - duration: BGM duration (default 20 seconds)
    
#     Response:
#         {
#             "analysis": {
#                 "emotion_timeline": [...],
#                 "dominant_emotion": "Happy",
#                 ...
#             },
#             "bgm": {
#                 "audio_url": "/static/generated/bgm_filename.wav",
#                 "emotion": "Happy",
#                 "duration": 20,
#                 "bpm": 120
#             },
#             "success": true
#         }
#     """
#     try:
#         video_path = None
        
#         # Check if video file is uploaded
#         if 'file' in request.files:
#             file = request.files['file']
            
#             if file.filename == '':
#                 return jsonify({'error': 'No file selected'}), 400
            
#             if not allowed_video_file(file.filename):
#                 return jsonify({'error': 'Invalid video file type'}), 400
            
#             # Save video file
#             filename = secure_filename(file.filename)
#             video_path = os.path.join(Config.UPLOAD_FOLDER, filename)
#             file.save(video_path)
            
#             # Get duration from form
#             bgm_duration = int(request.form.get('duration', 20))
        
#         # Check if video path is provided
#         elif request.is_json and 'video_path' in request.json:
#             video_path = request.json['video_path']
#             bgm_duration = request.json.get('duration', 20)
            
#             if not os.path.exists(video_path):
#                 return jsonify({'error': 'Video file not found'}), 400
        
#         else:
#             return jsonify({'error': 'No video file provided'}), 400
        
#         print(f"🎥 Analyzing video: {video_path}")
        
#         # Analyze video emotions
#         analysis = video_service.analyze_video_emotions(video_path, fps=1)
        
#         if 'error' in analysis:
#             return jsonify(analysis), 400
        
#         dominant_emotion = analysis.get('dominant_emotion', 'neutral')
        
#         print(f"🎵 Generating {bgm_duration}s BGM for emotion: {dominant_emotion}")
        
#         # Generate BGM (20 seconds by default)
#         bgm_result = gemini_service.generate_bgm_sync(
#             emotion=dominant_emotion,
#             duration=bgm_duration
#         )
        
#         if 'error' in bgm_result:
#             return jsonify({
#                 'analysis': analysis,
#                 'bgm_error': bgm_result['error'],
#                 'success': False
#             }), 500
        
#         if not bgm_result.get('audio_data'):
#             return jsonify({
#                 'analysis': analysis,
#                 'bgm_error': 'No audio data generated',
#                 'success': False
#             }), 500
        
#         # Save BGM file
#         video_basename = os.path.basename(video_path)
#         bgm_filename = f"bgm_{os.path.splitext(video_basename)[0]}_{int(time.time())}.wav"
#         bgm_filepath = os.path.join(Config.GENERATED_FOLDER, bgm_filename)
        
#         if gemini_service.save_bgm_to_file(bgm_result['audio_data'], bgm_filepath):
#             return jsonify({
#                 'analysis': analysis,
#                 'bgm': {
#                     'audio_url': f'/static/generated/{bgm_filename}',
#                     'emotion': dominant_emotion,
#                     'duration': bgm_result.get('duration', bgm_duration),
#                     'bpm': bgm_result.get('bpm'),
#                     'file_size_mb': bgm_result.get('file_size_mb'),
#                     'prompt': bgm_result.get('prompt')
#                 },
#                 'success': True
#             }), 200
#         else:
#             return jsonify({
#                 'analysis': analysis,
#                 'bgm_error': 'Failed to save BGM file',
#                 'success': False
#             }), 500
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @video_bp.route('/generate-bgm-emotion', methods=['POST'])
# def generate_bgm_for_emotion():
#     """
#     Generate 20-second background music for a specific emotion (no video required)
    
#     Request:
#         {
#             "emotion": "Happy",
#             "bpm": 120 (optional),
#             "temperature": 1.0 (optional),
#             "duration": 20 (optional, default 20 seconds)
#         }
    
#     Response:
#         {
#             "audio_url": "/static/generated/bgm_happy_xxx.wav",
#             "emotion": "Happy",
#             "duration": 20,
#             "bpm": 120
#         }
#     """
#     try:
#         data = request.json
        
#         if not data or 'emotion' not in data:
#             return jsonify({'error': 'Emotion is required'}), 400
        
#         emotion = data['emotion']
#         bpm = data.get('bpm', None)
#         temperature = data.get('temperature', 1.0)
#         duration = data.get('duration', 20)  # Default 20 seconds
        
#         # Validate parameters
#         if temperature < 0.0 or temperature > 2.0:
#             temperature = 1.0
        
#         if duration < 5 or duration > 60:
#             duration = 20
        
#         # Generate BGM
#         result = gemini_service.generate_bgm_sync(
#             emotion=emotion,
#             bpm=bpm,
#             temperature=temperature,
#             duration=duration
#         )
        
#         if 'error' in result:
#             return jsonify(result), 500
        
#         if not result.get('audio_data'):
#             return jsonify({'error': 'No audio data generated'}), 500
        
#         # Save to file
#         audio_filename = f"bgm_{emotion.lower()}_{duration}s_{int(time.time())}.wav"
#         audio_path = os.path.join(Config.GENERATED_FOLDER, audio_filename)
        
#         if gemini_service.save_bgm_to_file(result['audio_data'], audio_path):
#             return jsonify({
#                 'success': True,
#                 'audio_url': f'/static/generated/{audio_filename}',
#                 'emotion': emotion,
#                 'duration': result.get('duration', duration),
#                 'bpm': result.get('bpm'),
#                 'file_size_mb': result.get('file_size_mb'),
#                 'prompt': result.get('prompt')
#             }), 200
#         else:
#             return jsonify({'error': 'Failed to save audio file'}), 500
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @video_bp.route('/download-bgm/<filename>', methods=['GET'])
# def download_bgm(filename):
#     """
#     Download generated BGM file
    
#     URL: /api/video/download-bgm/<filename>
#     """
#     try:
#         filepath = os.path.join(Config.GENERATED_FOLDER, filename)
        
#         if not os.path.exists(filepath):
#             return jsonify({'error': 'File not found'}), 404
        
#         return send_file(filepath, as_attachment=True)
    
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from services.video_service import video_service
from services.gemini_service import gemini_service
from config import Config
import base64
import time

video_bp = Blueprint('video', __name__)

def allowed_video_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'mp4', 'avi', 'mov', 'mkv', 'webm'}

@video_bp.route('/analyze', methods=['POST'])
def analyze_video():
    """
    Analyze emotions in a video
    
    Request:
        - file: video file (multipart/form-data)
        - fps: frames per second to analyze (optional, default 1)
    
    Response:
        {
            "emotion_timeline": [...],
            "dominant_emotion": "Happy",
            "dominant_percentage": 65.5,
            "emotion_distribution": {...},
            "total_frames_analyzed": 30,
            "video_duration": 30.5
        }
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No video file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_video_file(file.filename):
            return jsonify({'error': 'Invalid video file type'}), 400
        
        fps = request.form.get('fps', 1)
        try:
            fps = int(fps)
        except:
            fps = 1
        
        # Save video file
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Analyze video emotions
        result = video_service.analyze_video_emotions(filepath, fps=fps)
        
        if 'error' in result:
            return jsonify(result), 400
        
        result['video_filename'] = filename
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@video_bp.route('/generate-bgm', methods=['POST'])
def generate_bgm():
    """
    Generate 20-second background music for video based on emotions
    
    Request:
        - file: video file (multipart/form-data)
        OR
        - video_path: path to already uploaded video (JSON)
        
        Optional:
        - fps: frames per second for analysis (default 1)
        - duration: BGM duration (default 20 seconds)
    
    Response:
        {
            "analysis": {
                "emotion_timeline": [...],
                "dominant_emotion": "Happy",
                ...
            },
            "bgm": {
                "audio_url": "/static/generated/bgm_filename.wav",
                "emotion": "Happy",
                "duration": 20,
                "bpm": 120
            },
            "success": true
        }
    """
    try:
        video_path = None
        
        # Check if video file is uploaded
        if 'file' in request.files:
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            if not allowed_video_file(file.filename):
                return jsonify({'error': 'Invalid video file type'}), 400
            
            # Save video file
            filename = secure_filename(file.filename)
            video_path = os.path.join(Config.UPLOAD_FOLDER, filename)
            file.save(video_path)
            
            # Get duration from form
            bgm_duration = int(request.form.get('duration', 20))
        
        # Check if video path is provided
        elif request.is_json and 'video_path' in request.json:
            video_path = request.json['video_path']
            bgm_duration = request.json.get('duration', 20)
            
            if not os.path.exists(video_path):
                return jsonify({'error': 'Video file not found'}), 400
        
        else:
            return jsonify({'error': 'No video file provided'}), 400
        
        print(f"🎥 Analyzing video: {video_path}")
        
        # Analyze video emotions
        analysis = video_service.analyze_video_emotions(video_path, fps=1)
        
        if 'error' in analysis:
            return jsonify(analysis), 400
        
        dominant_emotion = analysis.get('dominant_emotion', 'neutral')
        
        print(f"🎵 Generating {bgm_duration}s BGM for emotion: {dominant_emotion}")
        
        # Generate BGM (20 seconds by default)
        bgm_result = gemini_service.generate_bgm_sync(
            emotion=dominant_emotion,
            duration=bgm_duration
        )
        
        if 'error' in bgm_result:
            return jsonify({
                'analysis': analysis,
                'bgm_error': bgm_result['error'],
                'success': False
            }), 500
        
        if not bgm_result.get('audio_data'):
            return jsonify({
                'analysis': analysis,
                'bgm_error': 'No audio data generated',
                'success': False
            }), 500
        
        # Save BGM file
        video_basename = os.path.basename(video_path)
        bgm_filename = f"bgm_{os.path.splitext(video_basename)[0]}_{int(time.time())}.wav"
        bgm_filepath = os.path.join(Config.GENERATED_FOLDER, bgm_filename)
        
        if gemini_service.save_bgm_to_file(bgm_result['audio_data'], bgm_filepath):
            # AUTO-PLAY in local media player
            gemini_service.play_audio_file(bgm_filepath)
            
            return jsonify({
                'analysis': analysis,
                'bgm': {
                    'audio_url': f'/static/generated/{bgm_filename}',
                    'emotion': dominant_emotion,
                    'duration': bgm_result.get('duration', bgm_duration),
                    'bpm': bgm_result.get('bpm'),
                    'file_size_mb': bgm_result.get('file_size_mb'),
                    'prompt': bgm_result.get('prompt')
                },
                'success': True
            }), 200
        else:
            return jsonify({
                'analysis': analysis,
                'bgm_error': 'Failed to save BGM file',
                'success': False
            }), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@video_bp.route('/generate-bgm-emotion', methods=['POST'])
def generate_bgm_for_emotion():
    """
    Generate 20-second background music for a specific emotion (no video required)
    
    Request:
        {
            "emotion": "Happy",
            "bpm": 120 (optional),
            "temperature": 1.0 (optional),
            "duration": 20 (optional, default 20 seconds)
        }
    
    Response:
        {
            "audio_url": "/static/generated/bgm_happy_xxx.wav",
            "emotion": "Happy",
            "duration": 20,
            "bpm": 120
        }
    """
    try:
        data = request.json
        
        if not data or 'emotion' not in data:
            return jsonify({'error': 'Emotion is required'}), 400
        
        emotion = data['emotion']
        bpm = data.get('bpm', None)
        temperature = data.get('temperature', 1.0)
        duration = data.get('duration', 20)  # Default 20 seconds
        
        # Validate parameters
        if temperature < 0.0 or temperature > 2.0:
            temperature = 1.0
        
        if duration < 5 or duration > 60:
            duration = 20
        
        # Generate BGM
        result = gemini_service.generate_bgm_sync(
            emotion=emotion,
            bpm=bpm,
            temperature=temperature,
            duration=duration
        )
        
        if 'error' in result:
            return jsonify(result), 500
        
        if not result.get('audio_data'):
            return jsonify({'error': 'No audio data generated'}), 500
        
        # Save to file
        audio_filename = f"bgm_{emotion.lower()}_{duration}s_{int(time.time())}.wav"
        audio_path = os.path.join(Config.GENERATED_FOLDER, audio_filename)
        
        if gemini_service.save_bgm_to_file(result['audio_data'], audio_path):
            return jsonify({
                'success': True,
                'audio_url': f'/static/generated/{audio_filename}',
                'emotion': emotion,
                'duration': result.get('duration', duration),
                'bpm': result.get('bpm'),
                'file_size_mb': result.get('file_size_mb'),
                'prompt': result.get('prompt')
            }), 200
        else:
            return jsonify({'error': 'Failed to save audio file'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@video_bp.route('/download-bgm/<filename>', methods=['GET'])
def download_bgm(filename):
    """
    Download generated BGM file
    
    URL: /api/video/download-bgm/<filename>
    """
    try:
        filepath = os.path.join(Config.GENERATED_FOLDER, filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(filepath, as_attachment=True)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500