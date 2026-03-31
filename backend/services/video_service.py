import cv2
import os
from PIL import Image
import numpy as np
from services.emotion_service import emotion_service
from services.gemini_service import gemini_service
from config import Config
import base64

class VideoService:
    def __init__(self):
        self.emotion_service = emotion_service
        self.gemini_service = gemini_service
    
    def extract_frames(self, video_path, fps=1):
        """
        Extract frames from video at specified FPS
        
        Args:
            video_path: Path to video file
            fps: Frames per second to extract (default: 1)
        
        Returns:
            list of tuples (timestamp, frame_array)
        """
        try:
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                print(f"Error opening video: {video_path}")
                return []
            
            video_fps = cap.get(cv2.CAP_PROP_FPS)
            frame_interval = int(video_fps / fps)
            
            frames = []
            frame_count = 0
            
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                if frame_count % frame_interval == 0:
                    timestamp = frame_count / video_fps
                    frames.append((timestamp, frame))
                
                frame_count += 1
            
            cap.release()
            print(f"Extracted {len(frames)} frames from video")
            
            return frames
            
        except Exception as e:
            print(f"Error extracting frames: {str(e)}")
            return []
    
    def analyze_video_emotions(self, video_path, fps=1):
        """
        Analyze emotions throughout a video
        
        Args:
            video_path: Path to video file
            fps: Frames per second to analyze
        
        Returns:
            dict with emotion timeline and dominant emotion
        """
        try:
            # Extract frames
            frames = self.extract_frames(video_path, fps)
            
            if not frames:
                return {
                    'error': 'Could not extract frames from video',
                    'emotion_timeline': []
                }
            
            # Analyze each frame
            emotion_timeline = []
            emotion_counts = {}
            
            for timestamp, frame in frames:
                # Detect emotion in frame
                result = self.emotion_service.detect_from_frame(frame)
                
                if result.get('face_detected'):
                    emotion_data = {
                        'timestamp': round(timestamp, 2),
                        'emotion': result['top_emotion'],
                        'confidence': result['confidence'],
                        'all_emotions': result['emotions']
                    }
                    emotion_timeline.append(emotion_data)
                    
                    # Count emotions
                    emotion = result['top_emotion']
                    emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            # Determine dominant emotion
            if emotion_counts:
                dominant_emotion = max(emotion_counts, key=emotion_counts.get)
                total_frames = len(emotion_timeline)
                dominant_percentage = (emotion_counts[dominant_emotion] / total_frames) * 100
            else:
                dominant_emotion = 'neutral'
                dominant_percentage = 0
            
            return {
                'emotion_timeline': emotion_timeline,
                'dominant_emotion': dominant_emotion,
                'dominant_percentage': round(dominant_percentage, 2),
                'emotion_distribution': emotion_counts,
                'total_frames_analyzed': len(emotion_timeline),
                'video_duration': frames[-1][0] if frames else 0
            }
            
        except Exception as e:
            print(f"Error analyzing video emotions: {str(e)}")
            return {
                'error': str(e),
                'emotion_timeline': []
            }
    
    def generate_video_bgm(self, video_path, output_path=None):
        """
        Generate background music for video based on emotions
        
        Args:
            video_path: Path to video file
            output_path: Path to save generated audio (optional)
        
        Returns:
            dict with BGM data and emotion analysis
        """
        try:
            # Analyze video emotions
            print("Analyzing video emotions...")
            analysis = self.analyze_video_emotions(video_path, fps=1)
            
            if 'error' in analysis:
                return analysis
            
            # Get video duration
            video_duration = analysis.get('video_duration', 30)
            dominant_emotion = analysis.get('dominant_emotion', 'neutral')
            
            print(f"Dominant emotion: {dominant_emotion}")
            print(f"Video duration: {video_duration}s")
            
            # Generate BGM using Gemini
            print("Generating background music...")
            bgm_result = self.gemini_service.generate_bgm_sync(
                emotion=dominant_emotion,
                duration=int(video_duration)
            )
            
            if 'error' in bgm_result:
                return {
                    'error': bgm_result['error'],
                    'analysis': analysis
                }
            
            # Save audio if output path provided
            if output_path and bgm_result.get('audio_data'):
                try:
                    audio_bytes = base64.b64decode(bgm_result['audio_data'])
                    with open(output_path, 'wb') as f:
                        f.write(audio_bytes)
                    print(f"Audio saved to: {output_path}")
                except Exception as e:
                    print(f"Error saving audio: {str(e)}")
            
            return {
                'analysis': analysis,
                'bgm': bgm_result,
                'success': True
            }
            
        except Exception as e:
            print(f"Error generating video BGM: {str(e)}")
            return {
                'error': str(e),
                'success': False
            }
    
    def create_emotion_segments(self, emotion_timeline, min_segment_duration=3):
        """
        Create emotion segments from timeline for multi-emotion BGM
        
        Args:
            emotion_timeline: list of emotion data with timestamps
            min_segment_duration: minimum duration for a segment (seconds)
        
        Returns:
            list of emotion segments with start, duration, and emotion
        """
        if not emotion_timeline:
            return []
        
        segments = []
        current_emotion = emotion_timeline[0]['emotion']
        segment_start = emotion_timeline[0]['timestamp']
        
        for i, frame_data in enumerate(emotion_timeline[1:], 1):
            emotion = frame_data['emotion']
            timestamp = frame_data['timestamp']
            
            # If emotion changed and segment is long enough
            if emotion != current_emotion:
                duration = timestamp - segment_start
                
                if duration >= min_segment_duration:
                    segments.append({
                        'emotion': current_emotion,
                        'start': segment_start,
                        'duration': duration
                    })
                    current_emotion = emotion
                    segment_start = timestamp
        
        # Add final segment
        if emotion_timeline:
            final_duration = emotion_timeline[-1]['timestamp'] - segment_start
            if final_duration >= min_segment_duration:
                segments.append({
                    'emotion': current_emotion,
                    'start': segment_start,
                    'duration': final_duration
                })
        
        return segments

# Singleton instance
video_service = VideoService()