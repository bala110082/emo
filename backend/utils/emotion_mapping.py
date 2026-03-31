# Emotion to Genre Mapping

# Simple emotion to genre mapping
EMOTION_TO_GENRE_MAPPING = {
    'happy': ['pop', 'dance', 'happy', 'disco', 'funk'],
    'sad': ['blues', 'acoustic', 'sad', 'folk', 'ballad'],
    'angry': ['rock', 'metal', 'hard-rock', 'punk-rock', 'heavy-metal'],
    'fear': ['hip-hop', 'trap', 'industrial', 'dark-ambient'],
    'disgust': ['grunge', 'alternative', 'post-punk'],
    'surprise': ['edm', 'house', 'dance', 'electronic', 'techno'],
    'neutral': ['chill', 'ambient', 'lo-fi', 'instrumental', 'minimal-techno']
}

# Combined sentiment + emotion mapping (from original code)
COMBINED_LABELS = {
    "POS_love": ["r-n-b", "soul", "romance", "classic pakistani pop"],
    "NEG_love": ["alt-rock", "emo", "sad"],
    "POS_joy": ["pop", "dance", "happy", "modern bollywood", "sufi", "chill", "ambient"],
    "NEG_joy": ["indie", "emo", "sad"],
    "POS_sadness": ["folk", "blues", "acoustic"],
    "NEG_sadness": ["emo", "grunge", "black-metal"],
    "POS_anger": ["rock", "hard-rock", "metal"],
    "NEG_anger": ["punk-rock", "hardcore", "metalcore"],
    "POS_fear": ["hip-hop", "trap", "rap"],
    "NEG_fear": ["heavy-metal", "death-metal", "industrial"],
    "POS_surprise": ["dance", "edm", "house"],
    "NEG_surprise": ["electronic", "ambient", "minimal-techno"],
    "NEU_love": ["r-n-b", "soul"],
    "NEU_joy": ["pop", "dance", "sufi", "chill", "ambient"],
    "NEU_sadness": ["folk", "blues"],
    "NEU_anger": ["rock", "hard-rock"],
    "NEU_fear": ["hip-hop", "rap"],
    "NEU_surprise": ["dance", "house"],
    # Additional mappings for our emotion classes
    "POS_happy": ["pop", "dance", "happy", "disco", "funk"],
    "NEG_happy": ["indie", "alternative"],
    "NEU_happy": ["pop", "chill"],
    "POS_sad": ["folk", "blues", "acoustic"],
    "NEG_sad": ["emo", "grunge"],
    "NEU_sad": ["folk", "ambient"],
    "POS_angry": ["rock", "hard-rock"],
    "NEG_angry": ["metal", "punk-rock", "hardcore"],
    "NEU_angry": ["rock", "alternative"],
    "POS_disgust": ["alternative", "indie"],
    "NEG_disgust": ["grunge", "industrial"],
    "NEU_disgust": ["alternative"],
    "POS_neutral": ["chill", "ambient", "lo-fi"],
    "NEG_neutral": ["minimal-techno", "ambient"],
    "NEU_neutral": ["ambient", "instrumental"]
}

# Emotion to sentiment mapping (for text-based analysis)
EMOTION_SENTIMENT_MAPPING = {
    'happy': 'POS',
    'joy': 'POS',
    'love': 'POS',
    'sad': 'NEG',
    'sadness': 'NEG',
    'angry': 'NEG',
    'anger': 'NEG',
    'fear': 'NEG',
    'disgust': 'NEG',
    'surprise': 'NEU',
    'neutral': 'NEU'
}

def get_genres_for_emotion(emotion, sentiment='POS'):
    """
    Get genre list for a given emotion and sentiment
    
    Args:
        emotion: str (emotion name)
        sentiment: str (POS, NEG, NEU)
    
    Returns:
        list of genre strings
    """
    emotion_lower = emotion.lower()
    
    # Try combined label first
    key = f"{sentiment}_{emotion_lower}"
    if key in COMBINED_LABELS:
        return COMBINED_LABELS[key]
    
    # Fallback to simple mapping
    if emotion_lower in EMOTION_TO_GENRE_MAPPING:
        return EMOTION_TO_GENRE_MAPPING[emotion_lower]
    
    # Default fallback
    return ['pop', 'chill']

def get_sentiment_for_emotion(emotion):
    """
    Get sentiment (POS/NEG/NEU) for a given emotion
    
    Args:
        emotion: str (emotion name)
    
    Returns:
        str (POS, NEG, or NEU)
    """
    emotion_lower = emotion.lower()
    return EMOTION_SENTIMENT_MAPPING.get(emotion_lower, 'NEU')