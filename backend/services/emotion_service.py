import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np
import json
import cv2
from config import Config

# DeepFace import
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    DEEPFACE_AVAILABLE = False
    print("DeepFace not available. Install with: pip install deepface")

class EmotionService:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"Using device: {self.device}")
        
        # Load model info
        with open(Config.MODEL_INFO_PATH, 'r') as f:
            model_info = json.load(f)
        
        self.emotion_classes = model_info['emotion_classes']
        self.emotion_to_label = model_info['emotion_to_label']
        self.label_to_emotion = {int(k): v for k, v in model_info['label_to_emotion'].items()}
        self.img_size = model_info['img_size']
        
        # Load custom emotion model
        self.model = self._load_custom_model()
        
        # Image transformation
        self.transform = transforms.Compose([
            transforms.Resize((self.img_size, self.img_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Face cascade
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        print("Emotion Service initialized successfully")
    
    def _load_custom_model(self):
        """Load the custom EfficientNet-B2 model"""
        model = models.efficientnet_b2(weights=None)
        num_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(p=0.3, inplace=True),
            nn.Linear(num_features, len(self.emotion_classes))
        )
        model.load_state_dict(
            torch.load(Config.EMOTION_MODEL_PATH, map_location=self.device)
        )
        model = model.to(self.device)
        model.eval()
        
        print(f"Custom model loaded with {len(self.emotion_classes)} emotion classes")
        return model
    
    def detect_face_haar(self, image):
        """Detect face using Haar Cascade"""
        try:
            # Convert PIL Image to numpy array
            image_np = np.array(image)
            
            # Convert RGB to grayscale
            if len(image_np.shape) == 3:
                gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
            else:
                gray = image_np
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                maxSize=(500, 500)
            )
            
            print(f"Haar Cascade detected {len(faces)} faces")
            
            if len(faces) == 0:
                return None, False
            
            # Get the largest face
            largest_face = max(faces, key=lambda face: face[2] * face[3])
            x, y, w, h = largest_face
            
            # Extract face region
            face = image.crop((x, y, x+w, y+h))
            
            print(f"Face detected at: ({x}, {y}, {w}, {h})")
            return face, True
            
        except Exception as e:
            print(f"Error in face detection: {str(e)}")
            return None, False
    
    def predict_emotion_custom(self, image):
        """Predict emotion using custom EfficientNet model"""
        try:
            print("Using custom EfficientNet model")
            
            if image.size[0] < 64 or image.size[1] < 64:
                print("Image too small!")
                return None
            
            # Transform image
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Predict
            with torch.no_grad():
                output = self.model(image_tensor)
                probabilities = torch.softmax(output, dim=1)
                probs = probabilities[0].cpu().numpy()
            
            # Create emotion probabilities dict
            emotion_probs = {
                self.label_to_emotion[i]: float(probs[i] * 100)
                for i in range(len(self.emotion_classes))
            }
            
            print(f"Custom model predictions: {emotion_probs}")
            return emotion_probs
            
        except Exception as e:
            print(f"Error in custom emotion prediction: {str(e)}")
            return None
    
    def predict_emotion_deepface(self, image):
        """Predict emotion using DeepFace library"""
        if not DEEPFACE_AVAILABLE:
            
            return self.predict_emotion_custom(image)
        
        try:
            
            
            # Convert PIL to numpy array
            image_np = np.array(image)
            
            # Convert RGB to BGR for OpenCV
            if len(image_np.shape) == 3 and image_np.shape[2] == 3:
                image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            else:
                image_bgr = image_np
            
            # Analyze emotions
            analysis = DeepFace.analyze(
                img_path=image_bgr,
                actions=['emotion'],
                enforce_detection=False,
                detector_backend='opencv'
            )
            
            # Extract emotions
            if isinstance(analysis, list):
                emotions = analysis[0]['emotion']
            else:
                emotions = analysis['emotion']
            
            # Map to your emotion classes
            emotion_probs = {}
            emotion_mapping = {
                'happy': 'Happy',
                'sad': 'Sad',
                'angry': 'Angry',
                'fear': 'Fear',
                'disgust': 'Disgust',
                'surprise': 'Surprise',
                'neutral': 'Neutral'
            }
            
            for deepface_emotion, prob in emotions.items():
                mapped_emotion = emotion_mapping.get(deepface_emotion.lower())
                if mapped_emotion:
                    emotion_probs[mapped_emotion] = float(prob)
            
            # Ensure all emotion classes are present
            for emotion_class in self.emotion_classes:
                if emotion_class not in emotion_probs:
                    emotion_probs[emotion_class] = 0.0
            
            print(f" predictions: {emotion_probs}")
            return emotion_probs
            
        except Exception as e:
            print(f"Error with DeepFace: {str(e)}")
            return self.predict_emotion_custom(image)
    
    def detect_from_image(self, image_path, use_deepface=False):
        """
        Main method to detect emotion from image path
        
        Args:
            image_path: Path to image file
            use_deepface: Whether to use DeepFace (for webcam) or custom model
        
        Returns:
            dict: {
                'emotions': dict of emotion probabilities,
                'top_emotion': str,
                'confidence': float,
                'face_detected': bool
            }
        """
        try:
            # Load image
            image = Image.open(image_path).convert('RGB')
            
            # Detect face
            face, face_detected = self.detect_face_haar(image)
            
            if not face_detected:
                return {
                    'error': 'No face detected',
                    'face_detected': False
                }
            
            # Predict emotion
            if use_deepface:
                emotion_probs = self.predict_emotion_deepface(face)
            else:
                emotion_probs = self.predict_emotion_custom(face)
            
            if emotion_probs is None:
                return {
                    'error': 'Unable to predict emotions',
                    'face_detected': True
                }
            
            # Get top emotion
            top_emotion = max(emotion_probs, key=emotion_probs.get)
            confidence = emotion_probs[top_emotion]
            
            return {
                'emotions': emotion_probs,
                'top_emotion': top_emotion,
                'confidence': round(confidence, 2),
                'face_detected': True
            }
            
        except Exception as e:
            print(f"Error in detect_from_image: {str(e)}")
            return {
                'error': str(e),
                'face_detected': False
            }
    
    def detect_from_frame(self, frame_array):
        """
        Detect emotion from numpy array (for video frames or webcam)
        
        Args:
            frame_array: numpy array (BGR format from OpenCV)
        
        Returns:
            dict: Same as detect_from_image
        """
        try:
            # Convert BGR to RGB
            if len(frame_array.shape) == 3:
                frame_rgb = cv2.cvtColor(frame_array, cv2.COLOR_BGR2RGB)
            else:
                frame_rgb = frame_array
            
            # Convert to PIL Image
            image = Image.fromarray(frame_rgb)
            
            # Detect face
            face, face_detected = self.detect_face_haar(image)
            
            if not face_detected:
                return {
                    'error': 'No face detected',
                    'face_detected': False
                }
            
            # Use DeepFace for real-time (faster)
            emotion_probs = self.predict_emotion_deepface(face)
            
            if emotion_probs is None:
                return {
                    'error': 'Unable to predict emotions',
                    'face_detected': True
                }
            
            top_emotion = max(emotion_probs, key=emotion_probs.get)
            confidence = emotion_probs[top_emotion]
            
            return {
                'emotions': emotion_probs,
                'top_emotion': top_emotion,
                'confidence': round(confidence, 2),
                'face_detected': True
            }
            
        except Exception as e:
            print(f"Error in detect_from_frame: {str(e)}")
            return {
                'error': str(e),
                'face_detected': False
            }

# Singleton instance
emotion_service = EmotionService()