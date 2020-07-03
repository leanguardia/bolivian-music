import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

def fetch_playlists(min_followers=0, store_csv=False):
    """ Retrieves playlists containing the keyword 'bolivia'.

       Parameters:
       - min_followers (int): Minimum number of followers to keep the item. 
       - store_csv (bool):    If true a csv file is stored.

       Returns:
       - playlists (dataframe): Returns a dataframe containing retrieved results. 
    """

    results = spotify.search(q='bolivia', type='playlist', limit=50)
    playlists = results['playlists']['items']
    data = _build_playlist_data()

    for playlist_simple in playlists:
        playlist = spotify.playlist(playlist_simple['id'])
        n_followers = playlist['followers']['total']
        if n_followers >= min_followers:
            data['id'].append(playlist['id'])
            data['name'].append(playlist['name'])
            data['followers'].append(n_followers)
            data['owner_name'].append(playlist['owner']['display_name'])
            data['owner_id'].append(playlist['owner']['id'])
            data['description'].append(playlist['description'])
        else:
            print('Discarding', playlist['id'])
    
    df = pd.DataFrame(data, columns=data.keys())
    if store_csv: df.to_csv('data/playlists.csv', index=False)
    return df

def _build_playlist_data():
    return {
        'id': [],
        'name': [],
        'followers': [],
        'owner_name': [],
        'owner_id': [],
        'description': [],
    }

if __name__ == "__main__":
    playlists = fetch_playlists()
