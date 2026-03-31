import torch
import torch.nn as nn
from torchvision import models, transforms
import json
from config import Config

class EmotionModel:
    """Wrapper class for emotion detection model"""
    
    def __init__(self, model_path=None, model_info_path=None):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load model info
        model_info_path = model_info_path or Config.MODEL_INFO_PATH
        with open(model_info_path, 'r') as f:
            self.model_info = json.load(f)
        
        self.emotion_classes = self.model_info['emotion_classes']
        self.emotion_to_label = self.model_info['emotion_to_label']
        self.label_to_emotion = {int(k): v for k, v in self.model_info['label_to_emotion'].items()}
        self.img_size = self.model_info['img_size']
        
        # Load model
        model_path = model_path or Config.EMOTION_MODEL_PATH
        self.model = self._build_model(model_path)
        
        # Transform
        self.transform = transforms.Compose([
            transforms.Resize((self.img_size, self.img_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        print(f"EmotionModel initialized on {self.device}")
    
    def _build_model(self, model_path):
        """Build and load the EfficientNet-B2 model"""
        model = models.efficientnet_b2(weights=None)
        num_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(p=0.3, inplace=True),
            nn.Linear(num_features, len(self.emotion_classes))
        )
        
        # Load weights
        model.load_state_dict(torch.load(model_path, map_location=self.device))
        model = model.to(self.device)
        model.eval()
        
        return model
    
    def predict(self, image):
        """
        Predict emotion from PIL Image
        
        Args:
            image: PIL Image
        
        Returns:
            dict: emotion probabilities
        """
        try:
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
            
            return emotion_probs
        
        except Exception as e:
            print(f"Error in prediction: {str(e)}")
            return None
    
    def get_top_emotion(self, emotion_probs):
        """Get the top emotion from probabilities"""
        if not emotion_probs:
            return None, 0.0
        
        top_emotion = max(emotion_probs, key=emotion_probs.get)
        confidence = emotion_probs[top_emotion]
        
        return top_emotion, confidence