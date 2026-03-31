import cv2
import os
import numpy as np
from moviepy.editor import VideoFileClip

def get_video_info(video_path):
    """
    Get video information
    
    Args:
        video_path: path to video file
    
    Returns:
        dict: video information
    """
    cap = cv2.VideoCapture(video_path)
    
    info = {
        'fps': cap.get(cv2.CAP_PROP_FPS),
        'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        'duration': cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    }
    
    cap.release()
    return info

def extract_frame_at_time(video_path, timestamp):
    """
    Extract frame at specific timestamp
    
    Args:
        video_path: path to video
        timestamp: time in seconds
    
    Returns:
        numpy array: frame
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_number = int(timestamp * fps)
    
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    
    cap.release()
    
    if ret:
        return frame
    return None

def save_frame(frame, output_path):
    """Save frame as image"""
    cv2.imwrite(output_path, frame)

def create_video_from_frames(frames, output_path, fps=30):
    """
    Create video from frames
    
    Args:
        frames: list of numpy arrays
        output_path: output video path
        fps: frames per second
    """
    if not frames:
        return
    
    height, width = frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    for frame in frames:
        out.write(frame)
    
    out.release()

def extract_audio_from_video(video_path, output_audio_path):
    """
    Extract audio from video
    
    Args:
        video_path: input video path
        output_audio_path: output audio path
    """
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        
        if audio:
            audio.write_audiofile(output_audio_path)
            audio.close()
        
        video.close()
        return True
    except Exception as e:
        print(f"Error extracting audio: {str(e)}")
        return False

def add_audio_to_video(video_path, audio_path, output_path):
    """
    Add audio to video
    
    Args:
        video_path: input video path
        audio_path: audio file path
        output_path: output video path
    """
    try:
        from moviepy.editor import VideoFileClip, AudioFileClip
        
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)
        
        # Trim audio to video length
        if audio.duration > video.duration:
            audio = audio.subclip(0, video.duration)
        
        video_with_audio = video.set_audio(audio)
        video_with_audio.write_videofile(output_path)
        
        video.close()
        audio.close()
        return True
    except Exception as e:
        print(f"Error adding audio: {str(e)}")
        return False

def resize_video(video_path, output_path, width=None, height=None):
    """
    Resize video
    
    Args:
        video_path: input video path
        output_path: output video path
        width: target width
        height: target height
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    if width is None and height is None:
        width, height = 640, 480
    elif width is None:
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) * height / cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    elif height is None:
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) * width / cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        resized = cv2.resize(frame, (width, height))
        out.write(resized)
    
    cap.release()
    out.release()

def validate_video(video_path):
    """
    Validate video file
    
    Args:
        video_path: path to video
    
    Returns:
        bool: True if valid
    """
    if not os.path.exists(video_path):
        return False
    
    cap = cv2.VideoCapture(video_path)
    is_valid = cap.isOpened()
    cap.release()
    
    return is_valid

def get_video_thumbnail(video_path, output_path=None, timestamp=1.0):
    """
    Extract thumbnail from video
    
    Args:
        video_path: path to video
        output_path: output image path
        timestamp: time in seconds
    
    Returns:
        numpy array: thumbnail frame
    """
    frame = extract_frame_at_time(video_path, timestamp)
    
    if frame is not None and output_path:
        save_frame(frame, output_path)
    
    return frame