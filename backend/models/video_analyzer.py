import cv2
import numpy as np
from collections import Counter

class VideoAnalyzer:
    """Video emotion analysis utilities"""
    
    def __init__(self, emotion_service):
        self.emotion_service = emotion_service
    
    def extract_frames(self, video_path, fps=1):
        """
        Extract frames from video at specified FPS
        
        Args:
            video_path: path to video file
            fps: frames per second to extract
        
        Returns:
            list of (timestamp, frame) tuples
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
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
        return frames
    
    def analyze_frames(self, frames):
        """
        Analyze emotions in frames
        
        Args:
            frames: list of (timestamp, frame) tuples
        
        Returns:
            list of emotion data
        """
        emotion_timeline = []
        
        for timestamp, frame in frames:
            result = self.emotion_service.detect_from_frame(frame)
            
            if result.get('face_detected'):
                emotion_timeline.append({
                    'timestamp': round(timestamp, 2),
                    'emotion': result['top_emotion'],
                    'confidence': result['confidence'],
                    'all_emotions': result['emotions']
                })
        
        return emotion_timeline
    
    def get_dominant_emotion(self, emotion_timeline):
        """
        Get dominant emotion from timeline
        
        Args:
            emotion_timeline: list of emotion data
        
        Returns:
            tuple: (dominant_emotion, percentage)
        """
        if not emotion_timeline:
            return 'neutral', 0.0
        
        emotions = [item['emotion'] for item in emotion_timeline]
        emotion_counts = Counter(emotions)
        
        dominant_emotion = emotion_counts.most_common(1)[0][0]
        dominant_count = emotion_counts[dominant_emotion]
        percentage = (dominant_count / len(emotions)) * 100
        
        return dominant_emotion, percentage
    
    def get_emotion_distribution(self, emotion_timeline):
        """
        Get emotion distribution
        
        Args:
            emotion_timeline: list of emotion data
        
        Returns:
            dict: emotion counts
        """
        emotions = [item['emotion'] for item in emotion_timeline]
        return dict(Counter(emotions))
    
    def create_segments(self, emotion_timeline, min_duration=3):
        """
        Create emotion segments for multi-emotion BGM
        
        Args:
            emotion_timeline: list of emotion data
            min_duration: minimum segment duration in seconds
        
        Returns:
            list of segments
        """
        if not emotion_timeline:
            return []
        
        segments = []
        current_emotion = emotion_timeline[0]['emotion']
        segment_start = emotion_timeline[0]['timestamp']
        
        for data in emotion_timeline[1:]:
            if data['emotion'] != current_emotion:
                duration = data['timestamp'] - segment_start
                
                if duration >= min_duration:
                    segments.append({
                        'emotion': current_emotion,
                        'start': segment_start,
                        'duration': duration
                    })
                    current_emotion = data['emotion']
                    segment_start = data['timestamp']
        
        # Add final segment
        if emotion_timeline:
            final_duration = emotion_timeline[-1]['timestamp'] - segment_start
            if final_duration >= min_duration:
                segments.append({
                    'emotion': current_emotion,
                    'start': segment_start,
                    'duration': final_duration
                })
        
        return segments