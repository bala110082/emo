import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import Config

class SpotifyService:
    """Dedicated Spotify API service"""
    
    def __init__(self):
        try:
            credentials = SpotifyClientCredentials(
                client_id=Config.SPOTIFY_CLIENT_ID,
                client_secret=Config.SPOTIFY_CLIENT_SECRET
            )
            self.sp = spotipy.Spotify(client_credentials_manager=credentials)
            print("SpotifyService initialized")
        except Exception as e:
            print(f"Error initializing Spotify: {str(e)}")
            self.sp = None
    
    def search_tracks(self, query, limit=10):
        """Search tracks by query"""
        if not self.sp:
            return []
        
        try:
            results = self.sp.search(q=query, type='track', limit=limit)
            return self._format_tracks(results['tracks']['items'])
        except Exception as e:
            print(f"Error searching tracks: {str(e)}")
            return []
    
    def search_by_genre(self, genre, limit=10):
        """Search tracks by genre"""
        query = f'genre:"{genre}"'
        return self.search_tracks(query, limit)
    
    def search_by_artist(self, artist_name, limit=10):
        """Search tracks by artist"""
        if not self.sp:
            return []
        
        try:
            query = f'artist:{artist_name}'
            results = self.sp.search(q=query, type='track', limit=limit)
            return self._format_tracks(results['tracks']['items'])
        except Exception as e:
            print(f"Error searching artist tracks: {str(e)}")
            return []
    
    def get_artist_info(self, artist_name):
        """Get artist information"""
        if not self.sp:
            return None
        
        try:
            results = self.sp.search(q=f'artist:{artist_name}', type='artist')
            if results['artists']['items']:
                return results['artists']['items'][0]
            return None
        except Exception as e:
            print(f"Error getting artist info: {str(e)}")
            return None
    
    def get_artist_genres(self, artist_name):
        """Get genres for an artist"""
        artist_info = self.get_artist_info(artist_name)
        if artist_info:
            return artist_info.get('genres', [])
        return []
    
    def get_track_info(self, track_id):
        """Get detailed track information"""
        if not self.sp:
            return None
        
        try:
            return self.sp.track(track_id)
        except Exception as e:
            print(f"Error getting track info: {str(e)}")
            return None
    
    def _format_tracks(self, tracks):
        """Format track data"""
        formatted = []
        
        for track in tracks:
            formatted.append({
                'id': track['id'],
                'name': track['name'],
                'artists': ', '.join([a['name'] for a in track['artists']]),
                'album': track['album']['name'],
                'preview_url': track.get('preview_url'),
                'external_url': track['external_urls']['spotify'],
                'album_cover': track['album']['images'][0]['url'] if track['album']['images'] else None,
                'duration_ms': track['duration_ms'],
                'popularity': track['popularity']
            })
        
        return formatted