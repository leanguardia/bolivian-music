import sys, getopt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

def fetch_artists(playlist_ids):
    """ Retrieves artists data from playlists'.

       Parameters:
       - playlist_ids (list): List of Spotify Playlist ids.

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
    df = df.sort_values(by='followers', ascending=False)
    return df

def clean_artists(df):
    """ Filter irrelevant playlists."""

    # Remove artists with same name.
    df = df.drop_duplicates(subset='name', keep='first')

    # Remove artists from other countries
    foreign_countries_re = 'argentin|chile|colombia|mexic|peru|uruguay'
    df = df[~df.genres.astype(str).str.contains(foreign_countries_re)]

    # Remove manually selected artists
    excluded_artists = pd.read_csv('data/artists_excluded.csv')
    df = df[~df.artist_id.isin(excluded_artists.artist_id)]

    # Manually add genres to artists
    df = _extend_genres(df)

    return df


def _extend_genres(df):
    assignments = [{
        'genre': 'folklore boliviano',
        'names': ['Andesur', 'Canto Popular', 'Antares', 'Bolivia', 'Banda Intercontinental Poopó']
    }, {
        'genre': 'hip hop boliviano',
        'names': ['Mc J Rap', 'Zckrap', 'Erick Claros']
    }, {
        'genre': 'latin pop',
        'names': ['Bolivia Band']
    }, {
        'genre': 'reggae en espanol',
        'names': ['Illapa Reggae']
    }]

    for assignment in assignments:
        genre, names = assignment['genre'], assignment['names']
        to_modify = df.name.isin(names)
        df[to_modify].genres.apply(lambda genres: genres.append(genre))

    return df


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


def main(args):
    command_sample = 'artists_collector.py -p <playlists_filepath> -c -o <output_filepath>'
    input_filepath = 'data/playlists_filtered.csv'
    clean_df = False
    output_filepath = 'data/artists.csv'
    store_csv = False
    
    try:
        opts, args = getopt.getopt(args,"p:cs:",["playlists","clean","store"])
    except getopt.GetoptError:
        print(command_sample)
        sys.exit(2)

    # Parse options and arguments
    for opt, arg in opts:
        if opt in ("-p", "--playlists"):
            input_filepath = arg or input_filepath
        elif opt in ("-c", "--clean"):
            clean_df = True
        elif opt in ("-s", "--store"):
            store_csv = True
            output_filepath = arg or output_filepath
        else:
            print("Unknown option:", opt)
            print(command_sample)
            sys.exit()

    print("Loading Playlists …")
    playlists = pd.read_csv(input_filepath)
    print("Exploring artists from {} playlists".format(playlists.shape[0]))
    df = fetch_artists(playlists.playlist_id)
    print("Fething Done: {} artists fetched".format(df.shape[0]))

    if clean_df:
        df = clean_artists(df)
        print("Cleaning Done: {} artists".format(df.shape[0]))

    # Store data to csv
    if store_csv: 
        print("Storing Data in {}".format(output_filepath))
        df.to_csv(output_filepath, index=False)

    return df


if __name__ == "__main__":
    artists_df = main(sys.argv[1:])
