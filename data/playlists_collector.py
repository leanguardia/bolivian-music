import sys, getopt, argparse, time

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

get_milli_time = lambda: int(round(time.time() * 1000))

def fetch_playlists(min_followers=0):
    """ Retrieves playlists data containing the keyword 'bolivia'.

       Parameters:
       - min_followers (int): Minimum number of followers verified to keep the item.

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
            data['playlist_id'].append(playlist['id'])
            data['name'].append(playlist['name'])
            data['followers'].append(n_followers)
            data['tracks'].append(playlist['tracks']['total'])
            data['owner_name'].append(playlist['owner']['display_name'])
            data['owner_id'].append(playlist['owner']['id'])
            data['description'].append(playlist['description'])
        else:
            print('Discarding', playlist['id'])
    
    df = pd.DataFrame(data, columns=data.keys())
    return df

def clean_playlists(df):
    """ Filter irrelevant playlists. """

    # Keep items with Bolivia in the name.
    # Exclude Lamento (Lamento Boliviano is an argentinian song).
    df = df[df.name.str.contains('olivia|OLIVIA') & ~df.name.str.contains('Lamento|lamento')]
    
    # Manually remove irrelevant playlists.
    remove_ids = [
        '37i9dQZEVXbJqfMFK4d691', # Bolivia Top 50
        '37i9dQZEVXbMTKZuy8ORFV', # Bolivia Viral 50
        '7xg9H8UArAZRNW4UbtkuYG', # TOP HITS BOLIVIA
        '321jPs2Obj2j8qzroYv4S2', # La Previa Dj Micky
        '37i9dQZF1DX2LWCSft2vqi', # Top Artistas 2019
        '3L0GTgyBzx3cITSPBqE5CE', # Top 50
        '37i9dQZF1DXcaON5GWABL3', # Top 2019
        '1OciHZQgk4kMSxhVYivJLQ', # Martin Stephenson And The Daintees – Boat To Bolvia
        '2MGqkd7u2u87tLLFyzJ7DH', # Bolivia Top 100
    ]
    df = df[~df.playlist_id.isin(remove_ids)]
    return df

def _build_playlist_data():
    return {
        'playlist_id': [],
        'name': [],
        'followers': [],
        'tracks': [],
        'owner_name': [],
        'owner_id': [],
        'description': [],
    }

def main(args):
    command_sample = 'playlist_collector.py -c -s data/playlists.csv'
    store_csv = True
    output_filepath = 'data/playlists-%s.csv' % get_milli_time()
    clean_df = False

    try:
        opts, args = getopt.getopt(args,"cs:",["clean","store"])
    except getopt.GetoptError:
        print(command_sample)
        sys.exit(2)

    # Parse options and arguments
    for opt, arg in opts:
        if opt in ("-c", "--clean"):
            clean_df = True
        elif opt in ("-s", "--store"):
            store_csv = True
            output_filepath = arg or output_filepath
        else:
            print("Unknown option:", opt)
            print(command_sample)
            sys.exit()

    print("Extract from Spotify…")
    df = fetch_playlists()
    if store_csv: 
        print("Storing Data in {}".format(output_filepath))
        df.to_csv(output_filepath, index=False)
    
    print("Fetching Done: {} playlists".format(df.shape[0]))

    # Clean and Filter elements
    if clean_df:
        df = clean_playlists(df)
        print("Cleaning Done: {} playlists".format(df.shape[0]))

    return df


if __name__ == "__main__":
    playlists_df = main(sys.argv[1:])
