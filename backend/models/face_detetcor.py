import cv2
import numpy as np
from PIL import Image

try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    DEEPFACE_AVAILABLE = False

class FaceDetector:
    """Face detection using Haar Cascade and optionally DeepFace"""
    
    def __init__(self):
        # Initialize Haar Cascade
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        print("FaceDetector initialized")
    
    def detect_haar(self, image):
        """
        Detect face using Haar Cascade
        
        Args:
            image: PIL Image
        
        Returns:
            tuple: (face_image, detected_bool)
        """
        try:
            # Convert PIL to numpy array
            image_np = np.array(image)
            
            # Convert to grayscale
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
            
            if len(faces) == 0:
                return None, False
            
            # Get largest face
            largest_face = max(faces, key=lambda f: f[2] * f[3])
            x, y, w, h = largest_face
            
            # Crop face
            face = image.crop((x, y, x+w, y+h))
            
            return face, True
        
        except Exception as e:
            print(f"Error in Haar face detection: {str(e)}")
            return None, False
    
    def detect_deepface(self, image):
        """
        Detect face using DeepFace
        
        Args:
            image: PIL Image or numpy array
        
        Returns:
            tuple: (face_image, detected_bool)
        """
        if not DEEPFACE_AVAILABLE:
            return self.detect_haar(image)
        
        try:
            # Convert to numpy if PIL
            if isinstance(image, Image.Image):
                image_np = np.array(image)
            else:
                image_np = image
            
            # Convert RGB to BGR for OpenCV
            if len(image_np.shape) == 3 and image_np.shape[2] == 3:
                image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
            else:
                image_bgr = image_np
            
            # Detect face
            faces = DeepFace.extract_faces(
                img_path=image_bgr,
                detector_backend='opencv',
                enforce_detection=False
            )
            
            if not faces or len(faces) == 0:
                return None, False
            
            # Get first face region
            face_data = faces[0]
            facial_area = face_data['facial_area']
            
            x = facial_area['x']
            y = facial_area['y']
            w = facial_area['w']
            h = facial_area['h']
            
            # Crop face
            if isinstance(image, Image.Image):
                face = image.crop((x, y, x+w, y+h))
            else:
                face_np = image_np[y:y+h, x:x+w]
                face = Image.fromarray(face_np)
            
            return face, True
        
        except Exception as e:
            print(f"Error in DeepFace detection: {str(e)}")
            return self.detect_haar(image)
    
    def detect(self, image, use_deepface=False):
        """
        Detect face using specified method
        
        Args:
            image: PIL Image
            use_deepface: bool
        
        Returns:
            tuple: (face_image, detected_bool)
        """
        if use_deepface:
            return self.detect_deepface(image)
        else:
            return self.detect_haar(image)