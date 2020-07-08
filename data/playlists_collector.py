import sys, getopt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

def fetch_playlists(min_followers=0):
    """ Retrieves playlists data containing the keyword 'bolivia'.

       Parameters:
       - min_followers (int): Minimum number of followers verified to keep the item. 
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

def main(args):
    store_csv = False
    output_filepath = 'data/playlists.csv'

    try:
        opts, args = getopt.getopt(args,"so:",["store","ofile="])
    except getopt.GetoptError:
        print('playlist_collector.py -s -o <filepath>')
        sys.exit(2)
    
    print("Pulling data from Spotify …")
    df = fetch_playlists()
    print("Done: {} playlists fetched".format(df.shape[0]))

    # Parse options and arguments
    for opt, arg in opts:
        if opt in ("-s", "store"):
            store_csv = True
        elif opt in ("-o", "--output"):
            output_filepath = arg or output_filepath
        else:
            print("playlist_collector.py -s -o data/playlist.csv")
            sys.exit()

    # Store data to csv
    if store_csv: 
        print("Storing Data in {}".format(output_filepath))
        df.to_csv(output_filepath, index=False)

    return df

if __name__ == "__main__":
    playlists_df = main(sys.argv[1:])
