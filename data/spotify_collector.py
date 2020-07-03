import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

def fetch_playlists():
    results = spotify.search(q='bolivia', type='playlist', limit=50)
    playlists = results['playlists']['items']
    data = _build_playlist_data()
    
    for playlist in playlists:
        data['id'].append(playlist['id'])
        data['name'].append(playlist['name'])
        data['owner_name'].append(playlist['owner']['display_name'])
        data['owner_id'].append(playlist['owner']['id'])
        data['description'].append(playlist['description'])
    
    df = pd.DataFrame(data, columns=data.keys())
    return df

def _build_playlist_data():
    return {
        'id': [],
        'name': [],
        'description': [],
        'owner_name': [],
        'owner_id': [],
    }

if __name__ == "__main__":
    playlists = fetch_playlists()
