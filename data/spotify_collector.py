import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

def fetch_playlists(min_followers=0, store_csv=False):
    """ Retrieves playlists data containing the keyword 'bolivia'.

       Parameters:
       - min_followers (int): Minimum number of followers to keep the item. 
       - store_csv (bool):    If true a csv file is stored.

       Returns:
       - playlists (dataframe): Returns a dataframe containing retrieved results. 
    """

    response = spotify.search(q='bolivia', type='playlist', limit=50)
    playlists = response['playlists']['items']
    data = _build_playlist_data()

    for playlist_simple in playlists:
        playlist = spotify.playlist(playlist_simple['id'])
        n_followers = playlist['followers']['total']
        if n_followers >= min_followers:
            data['id'].append(playlist['id'])
            data['name'].append(playlist['name'])
            data['followers'].append(n_followers)
            data['tracks'].append(playlist['tracks']['total'])
            data['owner_name'].append(playlist['owner']['display_name'])
            data['owner_id'].append(playlist['owner']['id'])
            data['description'].append(playlist['description'])
        else:
            print('Discarding', playlist['id'])
    
    df = pd.DataFrame(data, columns=data.keys())
    if store_csv: df.to_csv('data/playlists.csv', index=False)
    return df


def fetch_artists(playlist_ids, store_csv=False):
    """ Retrieves artists data from playlists'.

       Parameters:
       - playlist_ids (list): List of Spotify Playlist ids.
       - store_csv (bool):    If true a csv file is stored.

       Returns:
       - artists (dataframe): Returns a dataframe containing retrieved results.
    """

    artists_ids = set()

    for playlist_id in playlist_ids:
        response = spotify.playlist_tracks(
            playlist_id,
            fields="items.track.album(!available_markets)")

        for track_item in response['items']:
            track_artists_ids = _list_artist_ids(track_item['track'])
            artists_ids = artists_ids.union(track_artists_ids)

    data = _build_artists_data()
    artists_ids = list(artists_ids)
    
    num_batches = int(np.ceil(len(artists_ids) / 50)) # 50 is the maximum artists to be fetched in one req.
    ids_batches = np.array_split(artists_ids, num_batches)
    
    for ids_batch in ids_batches:
        artists_items = spotify.artists(ids_batch)['artists']
        for artist in artists_items:
            data['artist_id'].append(artist['id'])
            data['name'].append(artist['name'])
            data['followers'].append(artist['followers']['total'])
            data['popularity'].append(artist['popularity'])
            data['genres'].append(artist['genres'])

    df = pd.DataFrame(data, columns=data.keys())
    if store_csv: df.to_csv('data/artists.csv', index=False)
    return df

def _build_playlist_data():
    return {
        'id': [],
        'name': [],
        'followers': [],
        'tracks': [],
        'owner_name': [],
        'owner_id': [],
        'description': [],
    }

def _build_artists_data():
    return {
        'artist_id': [],
        'name': [],
        'popularity': [],
        'followers': [],
        'genres': [],
    }

def _list_artist_ids(track_item):
    ids = []
    artist_items = track_item['album']['artists']
    for artist_item in artist_items:
        ids.append(artist_item['id'])
    return ids


if __name__ == "__main__":
    # playlists_df = fetch_playlists()
    ply_ids = ['37i9dQZF1DXcU9MUSqc5Ok', '4Vo04i7qwfew7LtHukfAh8', '3b9zB3X9JQPxrznZD5lfxy', '03ZSUNsVsoAeZKExgjnhUB', '211g8JAEFEqB9HnJyqSA3R', '2XfYxfqzUZl1ZVIF1htNQk', '5q6nmqaLJqtiWJwbv9I8i0', '6UdNU7zliQhLYyYEe2pFYY', '3eWL716NDY8CSDVZvh8Udo', '2zvn0gdOKh4xiMTqn9CVAk', '773iDD9rdBq6B3bgzCwklP', '5X37Zv0r4RqMcrvup19NAI', '5F6eeNiqNLD6cdgJ7S9GWJ', '4HL8IlbzOCGx28j5zHkI9U', '7IhQX1r2MphH86UNtA4Llo', '6sGsiDWCrnnHWOoZ7YfJyF', '3MPXWgEKvDPicO1UeXOVDs', '7ed0JL48relXZcPGYd3v2S', '2uWefhSt0FzL1GuY5QAkXd', '2Rq5AIA81iwvXN1kVRE5Eb', '2leeQMfgdkIEcaKXCPdWZQ', '1Sl9Ov25YF5yMHvbtZSZqq', '61j7OdOYSOdPsSphgLSIoD', '5m0C3CDYhOt20lbyGLTpiy', '6kBnDt633T7ylfaRUdanU5', '2UE51y00U1F589ytZSq6gw', '6lZcXjIcYANzBtutXzXUHt', '6p55on67kcTyHOvBCJaQjj', '5KvklFtZxPGzukUyA2xQCT', '3mEcFXW5IE5IKxXQQBgO2F', '0t3mcXp84obQ94aePxoj9Z', '1d29qW0wQRs5Oqi8Fobj8X', '65vCOvbKY2rsOYUXdsEJyX', '3hIDaIALu7oy2rn7OM0i1n', '3IsL5jwux8IR0FFmQ0iO5C', '3YtUz8kPK4hs916Vy4qWVp', '3vhz7F0Q7KVmAcfvay1SCa']
    artists_df = fetch_artists(ply_ids, store_csv=True)
