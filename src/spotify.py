import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from flask import session
import psycopg2

load_dotenv()

database = os.getenv('DATABASE_URL')
connection = psycopg2.connect(database)


CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

oauth = SpotifyOAuth(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    redirect_uri = REDIRECT_URI,
    scope="user-top-read user-read-recently-played playlist-modify-private"
)


def get_user_recent_artists(spotify):
    artist_results = spotify.current_user_top_artists(limit=10)
    
    return [artist['name'] for artist in artist_results['items']]

def get_track_uri(song):
    spotify = get_spotify()
    query = (
        f'track:"{song["name"]}" '
        f'artist:"{song["artist"]}"'
    )

    results = spotify.search(
        q=query,
        type="track",
        limit=3
    )

    tracks = results["tracks"]["items"]

    for track in tracks:
        spotify_name = track["name"].lower()

        if (
            "live" not in spotify_name
            and "version" not in spotify_name
            and "remaster" not in spotify_name
            and "remix" not in spotify_name
            and "mix" not in spotify_name
            and "acoustic" not in spotify_name
        ):
            return track["uri"]

    return None

def create_spotify_playlist(songlist):
    spotify = get_spotify()
    uri_list = []
    title = songlist['title']
    
    cached_songs = get_cached_songs(songlist['songs'])
    

    for song in songlist['songs']:
        lower = song['name'].lower()
        if (
        "version" not in lower
        and "remaster" not in lower
        and "remix" not in lower
        and "revisit" not in lower
        and "mix" not in lower
        ):
            key= (song['name'].lower(),
                  song['artist'].lower())
            uri =cached_songs.get(key)
            
            if not uri:
                uri = get_track_uri(song)
                if uri:
                    save_song_to_database(song, uri)
            
            if uri and uri not in uri_list:
                uri_list.append(uri)
        
    playlist = spotify.current_user_playlist_create(
        name=f"Music Bingo - {title}",
        public=False
    )
    print('playlist created')
    
    spotify.playlist_add_items(
    playlist["id"],
    uri_list
    )
    
    return playlist

def get_cached_songs(songs):
    
    song_keys = [
        (song['name'].lower(), song['artist'].lower()) for song in songs
    ]
    conditions = []
    values = []
    
    for name, artist in song_keys:
        conditions.append(
            "(LOWER(title) = %s AND LOWER(artist_name)=%s)"
        )
        values.extend([name, artist])
    
    query = f"""
    SELECT
        title,
        artist_name,
        spotify_uri
    FROM songs
    WHERE {" OR ".join(conditions)}
    """
    
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
            results = cur.fetchall()
    return {
        (row[0].lower(), row[1].lower()): row[2] for row in results
    }
    
def get_db_conn():
    return psycopg2.connect(database)

def save_song_to_database(song, uri=None):

    name = song['name'].lower()
    artist = song['artist'].lower()

    query = """
        INSERT INTO songs (title, artist_name, spotify_uri)
        VALUES (%s, %s, %s)
        ON CONFLICT (title, artist_name)
        DO UPDATE SET
            spotify_uri = COALESCE(EXCLUDED.spotify_uri, songs.spotify_uri)
    """

    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (name, artist, uri))
    
def get_spotify():
    token_info = session.get('token_info')
    print(session)
    if not token_info:
        return None
    
    if oauth.is_token_expired(token_info):
        token_info = oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info
    return spotipy.Spotify(
        auth=token_info['access_token']
    )       

#song_results = spotify.current_user_recently_played(limit=20)

#for song in song_results['items']:
#    print(song['track']['name'])