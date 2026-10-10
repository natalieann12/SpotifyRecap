import json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import ibis

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='e1a7187555744a2c9e6bbb0924487004',
    client_secret='REDACTED_ROTATED_SECRET',
    redirect_uri='http://127.0.0.1:3000',
    scope='user-read-recently-played user-top-read user-read-playback-state'  # Adjust scopes based on what data you need
))

# # Load settings from settings.json
# with open('settings.json', 'r') as f:
#     settings = json.load(f)

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
#     client_id=settings['SPOTIFY_CLIENT_ID'],
#     client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET'),
#     redirect_uri=settings['REDIRECT_URI'],
#     scope='user-read-recently-played'  # Adjust scopes based on what data you need
# ))

# Now you can make API calls, for example:
top_tracks = sp.current_user_top_tracks(limit=20)
print(json.dumps(top_tracks, indent=2))

tracks_flat = []
for track in top_tracks['items']:
    tracks_flat.append({
        'track_name': track['name'],
        'track_id': track['id'],
        'popularity': track['popularity'],
        'artist_name': track['artists'][0]['name'],  # First artist
        'album_name': track['album']['name'],
        'release_date': track['album']['release_date']
        # Add whatever fields you want
    })

# Create Ibis table
tracks_table = ibis.memtable(tracks_flat)
tracks_table.head()

# Try with audio features
top_audio_features = sp.audio_features
print(json.dumps(top_audio_features, indent=2))

audio_features_flat = []
for feature in top_audio_features['items']:
    audio_features_flat.append({
        'track_acousticness': feature['acousticness'],
        'track_danceability': feature['danceability'],
        'track_energy': feature['energy'],
        'track_instrumentalness': feature['instrumentalness'],
        'track_liveness': feature['liveness'],
        'track_mode': feature['mode'],
        'track_tempo': feature['tempo'],
        'track_time_signature': feature['time_signature'],
        'track_valence': feature['valence'],
        'track_id': feature['id'],
        'popularity': track['popularity'],
        'artist_name': track['artists'][0]['name'],  # First artist
        'album_name': track['album']['name'],
        'release_date': track['album']['release_date']
        # Add whatever fields you want
    })

# Create Ibis table
tracks_table = ibis.memtable(tracks_flat)
tracks_table.head()
