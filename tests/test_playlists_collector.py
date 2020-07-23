import data.playlists_collector as pc

def test_empty_playlist_container():
    empty_container = {
        'playlist_id': [],
        'name': [],
        'followers': [],
        'tracks': [],
        'owner_name': [],
        'owner_id': [],
        'description': [],
    }
    assert pc._build_playlist_data() == empty_container, "Do not match"
