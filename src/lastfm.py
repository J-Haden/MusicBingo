import requests   

API_KEY = '556cc517d2796b2ddcbf3bc95d14e8cf'

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

def get_top_tracks(artist):
    song_list=[]
    
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
            name_lower = name.lower()
            if (
                "version" not in name_lower
                and "remaster" not in name_lower
                and "remix" not in name_lower
                and "revisit" not in name_lower
                and "mix" not in name_lower
            ):
                song_list.append(track['name'])
    
    songs = list(dict.fromkeys(song_list))
    return songs[:75]







