import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import Config
from utils.emotion_mapping import EMOTION_TO_GENRE_MAPPING, COMBINED_LABELS
from Levenshtein import distance

class MusicService:
    def __init__(self):
        # Initialize Spotify client
        try:
            spotify_credentials = SpotifyClientCredentials(
                client_id=Config.SPOTIFY_CLIENT_ID,
                client_secret=Config.SPOTIFY_CLIENT_SECRET
            )
            self.sp = spotipy.Spotify(client_credentials_manager=spotify_credentials)
            print("Spotify API initialized successfully")
        except Exception as e:
            print(f"Error initializing Spotify: {str(e)}")
            self.sp = None
    
    def find_closest_genre(self, input_genre, genres):
        """Find the closest matching genre using Levenshtein distance"""
        min_distance = float('inf')
        closest_genres = []
        
        for genre in genres:
            d = distance(input_genre.lower(), genre.lower())
            if d < min_distance:
                min_distance = d
                closest_genres = [genre]
            elif d == min_distance:
                closest_genres.append(genre)
        
        return closest_genres
    
    def get_artist_genres(self, artist_name):
        """Get genres for a specific artist"""
        if not self.sp:
            return []
        
        try:
            results = self.sp.search(q=f'artist:{artist_name}', type='artist')
            
            if results['artists']['items']:
                artist_genres = results['artists']['items'][0]['genres']
                return artist_genres
            else:
                print(f"No artist found: {artist_name}")
                return []
        except Exception as e:
            print(f"Error getting artist genres: {str(e)}")
            return []
    
    def search_tracks_by_genre(self, genres, limit=10):
        """Search for tracks by genre list"""
        if not self.sp:
            return []
        
        try:
            if isinstance(genres, list) and len(genres) > 0:
                genre = genres[0]
            else:
                genre = genres
            
            # Build search query
            query = f'genre:"{genre}"'
            results = self.sp.search(q=query, type='track', limit=limit)
            
            tracks = []
            for track in results['tracks']['items']:
                track_info = {
                    'name': track['name'],
                    'artists': ', '.join([artist['name'] for artist in track['artists']]),
                    'album': track['album']['name'],
                    'preview_url': track['preview_url'],
                    'external_url': track['external_urls']['spotify'],
                    'album_cover': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'duration_ms': track['duration_ms'],
                    'popularity': track['popularity']
                }
                tracks.append(track_info)
            
            return tracks
            
        except Exception as e:
            print(f"Error searching tracks: {str(e)}")
            return []
    
    def recommend_by_emotion(self, emotion, sentiment='POS', limit=10):
        """
        Recommend music based on emotion and sentiment
        
        Args:
            emotion: str (Happy, Sad, Angry, Fear, etc.)
            sentiment: str (POS, NEG, NEU)
            limit: int (number of tracks to return)
        
        Returns:
            list of track dicts
        """
        try:
            # Get genres for this emotion-sentiment combination
            genre_key = f"{sentiment}_{emotion.lower()}"
            genres = COMBINED_LABELS.get(genre_key, [])
            
            if not genres:
                # Fallback to simple emotion mapping
                genres = EMOTION_TO_GENRE_MAPPING.get(emotion.lower(), ['pop'])
            
            print(f"Searching for genres: {genres}")
            
            # Search for tracks in these genres
            all_tracks = []
            tracks_per_genre = max(1, limit // len(genres))
            
            for genre in genres:
                tracks = self.search_tracks_by_genre(genre, limit=tracks_per_genre)
                all_tracks.extend(tracks)
            
            # Remove duplicates and limit
            unique_tracks = []
            seen_names = set()
            
            for track in all_tracks:
                track_id = (track['name'], track['artists'])
                if track_id not in seen_names:
                    seen_names.add(track_id)
                    unique_tracks.append(track)
                
                if len(unique_tracks) >= limit:
                    break
            
            return unique_tracks
            
        except Exception as e:
            print(f"Error in recommend_by_emotion: {str(e)}")
            return []
    
    def recommend_by_artist(self, artist_name, emotion, sentiment='POS', limit=10):
        """
        Recommend tracks from a specific artist filtered by emotion
        
        Args:
            artist_name: str
            emotion: str
            sentiment: str
            limit: int
        
        Returns:
            list of track dicts
        """
        if not self.sp:
            return []
        
        try:
            # Get artist's genres
            artist_genres = self.get_artist_genres(artist_name)
            
            if not artist_genres:
                return []
            
            # Get emotion genres
            genre_key = f"{sentiment}_{emotion.lower()}"
            emotion_genres = COMBINED_LABELS.get(genre_key, [])
            
            if not emotion_genres:
                emotion_genres = EMOTION_TO_GENRE_MAPPING.get(emotion.lower(), [])
            
            # Find matching genres
            matching_genres = []
            for emotion_genre in emotion_genres:
                closest = self.find_closest_genre(emotion_genre, artist_genres)
                matching_genres.extend(closest)
            
            # Search for artist tracks
            results = self.sp.search(q=f'artist:{artist_name}', type='track', limit=limit * 2)
            
            filtered_tracks = []
            for track in results['tracks']['items']:
                # Check if track matches emotion genres
                track_info = self.sp.track(track['id'])
                track_artists = track_info['artists']
                
                track_genres = []
                for artist in track_artists:
                    artist_info = self.sp.artist(artist['id'])
                    track_genres.extend(artist_info['genres'])
                
                # Check if any matching genre is in track genres
                if any(genre in track_genres for genre in matching_genres):
                    track_data = {
                        'name': track['name'],
                        'artists': ', '.join([a['name'] for a in track['artists']]),
                        'album': track['album']['name'],
                        'preview_url': track['preview_url'],
                        'external_url': track['external_urls']['spotify'],
                        'album_cover': track['album']['images'][0]['url'] if track['album']['images'] else None,
                        'duration_ms': track['duration_ms'],
                        'popularity': track['popularity']
                    }
                    filtered_tracks.append(track_data)
                
                if len(filtered_tracks) >= limit:
                    break
            
            return filtered_tracks
            
        except Exception as e:
            print(f"Error in recommend_by_artist: {str(e)}")
            return []
    
    def get_emotion_genres(self, emotion, sentiment='POS'):
        """Get the genre list for a given emotion and sentiment"""
        genre_key = f"{sentiment}_{emotion.lower()}"
        genres = COMBINED_LABELS.get(genre_key, [])
        
        if not genres:
            genres = EMOTION_TO_GENRE_MAPPING.get(emotion.lower(), ['pop'])
        
        return genres

# Singleton instance
music_service = MusicService()