from flask import Blueprint, request, jsonify
from services.music_service import music_service
from utils.emotion_mapping import get_genres_for_emotion, get_sentiment_for_emotion

music_bp = Blueprint('music', __name__)

@music_bp.route('/recommend', methods=['POST'])
def recommend_music():
    """
    Get music recommendations based on emotion
    
    Request:
        {
            "emotion": "Happy",
            "sentiment": "POS" (optional),
            "limit": 10 (optional)
        }
    
    Response:
        {
            "emotion": "Happy",
            "sentiment": "POS",
            "genres": ["pop", "dance", ...],
            "tracks": [
                {
                    "name": "Song Name",
                    "artists": "Artist Name",
                    "album": "Album Name",
                    "preview_url": "url",
                    "external_url": "spotify_url",
                    "album_cover": "image_url",
                    "duration_ms": 180000,
                    "popularity": 85
                },
                ...
            ]
        }
    """
    try:
        data = request.json
        
        if not data or 'emotion' not in data:
            return jsonify({'error': 'Emotion is required'}), 400
        
        emotion = data['emotion']
        sentiment = data.get('sentiment', 'POS')
        limit = data.get('limit', 10)
        
        # Validate inputs
        if not isinstance(limit, int) or limit < 1 or limit > 50:
            limit = 10
        
        # Get genres for this emotion
        genres = get_genres_for_emotion(emotion, sentiment)
        
        # Get music recommendations
        tracks = music_service.recommend_by_emotion(emotion, sentiment, limit)
        
        return jsonify({
            'emotion': emotion,
            'sentiment': sentiment,
            'genres': genres,
            'tracks': tracks,
            'count': len(tracks)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@music_bp.route('/recommend-artist', methods=['POST'])
def recommend_by_artist():
    """
    Get artist recommendations filtered by emotion
    
    Request:
        {
            "artist": "Artist Name",
            "emotion": "Happy",
            "sentiment": "POS" (optional),
            "limit": 10 (optional)
        }
    
    Response:
        {
            "artist": "Artist Name",
            "emotion": "Happy",
            "tracks": [...]
        }
    """
    try:
        data = request.json
        
        if not data or 'artist' not in data or 'emotion' not in data:
            return jsonify({'error': 'Artist and emotion are required'}), 400
        
        artist = data['artist']
        emotion = data['emotion']
        sentiment = data.get('sentiment', 'POS')
        limit = data.get('limit', 10)
        
        # Get artist recommendations
        tracks = music_service.recommend_by_artist(artist, emotion, sentiment, limit)
        
        return jsonify({
            'artist': artist,
            'emotion': emotion,
            'sentiment': sentiment,
            'tracks': tracks,
            'count': len(tracks)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@music_bp.route('/emotion-genres', methods=['GET'])
def get_emotion_genres():
    """
    Get genre mapping for an emotion
    
    Query params:
        - emotion: emotion name
        - sentiment: POS/NEG/NEU (optional)
    
    Response:
        {
            "emotion": "Happy",
            "sentiment": "POS",
            "genres": ["pop", "dance", ...]
        }
    """
    try:
        emotion = request.args.get('emotion')
        
        if not emotion:
            return jsonify({'error': 'Emotion parameter is required'}), 400
        
        sentiment = request.args.get('sentiment', 'POS')
        
        # Get genres
        genres = get_genres_for_emotion(emotion, sentiment)
        
        return jsonify({
            'emotion': emotion,
            'sentiment': sentiment,
            'genres': genres
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@music_bp.route('/detect-and-recommend', methods=['POST'])
def detect_and_recommend():
    """
    Combined endpoint: detect emotion from image and get recommendations
    
    Request:
        - file: image file
        OR
        - image: base64 encoded image
        
        Optional:
        - limit: number of tracks (default 10)
    
    Response:
        {
            "emotion_detection": {
                "emotions": {...},
                "top_emotion": "Happy",
                "confidence": 85.3
            },
            "music_recommendations": {
                "genres": [...],
                "tracks": [...]
            }
        }
    """
    try:
        # This endpoint would combine emotion detection and music recommendation
        # For now, return a message to use separate endpoints
        return jsonify({
            'message': 'Use /api/emotion/detect-image followed by /api/music/recommend',
            'example_flow': {
                '1': 'POST /api/emotion/detect-image with image',
                '2': 'Get emotion from response',
                '3': 'POST /api/music/recommend with emotion'
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@music_bp.route('/artist-genres', methods=['GET'])
def get_artist_genres():
    """
    Get genres for a specific artist
    
    Query params:
        - artist: artist name
    
    Response:
        {
            "artist": "Artist Name",
            "genres": ["pop", "rock", ...]
        }
    """
    try:
        artist = request.args.get('artist')
        
        if not artist:
            return jsonify({'error': 'Artist parameter is required'}), 400
        
        genres = music_service.get_artist_genres(artist)
        
        return jsonify({
            'artist': artist,
            'genres': genres
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500