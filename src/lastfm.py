import requests 
import dotenv
import os

dotenv.load_dotenv()  

API_KEY = os.getenv(LAST_API_KEY)

url = "https://ws.audioscrobbler.com/2.0/"


def get_top_artists(limit=10):
    params = {
        'method': 'chart.gettopartists',
        'api_key': API_KEY,
        'format': 'json',
        'limit': limit
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    artists=response.json()['artists']['artist']
    
    return [artist['name'] for artist in artists]

def get_top_tags():
    params = {
        "method": "tag.getTopTags",
        "api_key": API_KEY,
        "format": "json"
    }

    response = requests.get(url, params=params)

    tags = response.json()["toptags"]["tag"]

    return [
        {
            "name": tag["name"],
            "count": tag["count"]
        }
        for tag in tags
    ]

def get_top_tracks(artist):
    song_list=[]
    seen=set()
    
    for page in range(3):
        params = {
            "method": 'artist.getTopTracks', 
            'artist': artist,
            'api_key': API_KEY,
            'format': 'json', 
            'page': page
        }

        response = requests.get(url, params=params)

        tracks = response.json()['toptracks']['track']
        
        for track in tracks:
            name = track['name']
            performer = track['artist']['name']
            name_lower = name.lower()
            key=(name.lower(), performer.lower())
            if key in seen:
                continue
            if (
                "version" not in name_lower
                and "remaster" not in name_lower
                and "remix" not in name_lower
                and "revisit" not in name_lower
                and "mix" not in name_lower
            ):
                song_data = {'name': name, 'artist': performer}
                song_list.append(song_data)
            seen.add(key)
    
    return song_list[:75]

def get_tag_tracks(tag):
    song_list = []
    seen = set()
    
    for page in range(1, 4):
        params = {
            "method": 'tag.getTopTracks', 
            'tag': tag,
            'api_key': API_KEY,
            'format': 'json', 
            'page': page
        }

        response = requests.get(url, params=params)
        
        print(response.url)
        print(response.status_code)
        print(response.json())

        tracks = response.json()['tracks']['track']
        
        for track in tracks:
            name = track['name']
            performer = track['artist']['name']
            name_lower = name.lower()
            key=(name.lower(), performer.lower())
            if key in seen:
                continue
            if (
                "version" not in name_lower
                and "remaster" not in name_lower
                and "remix" not in name_lower
                and "revisit" not in name_lower
                and "mix" not in name_lower
            ):
                song_data = {'name': name, 'artist': performer}
                song_list.append(song_data)
            seen.add(key)
    
    return song_list[:75]
    
        







