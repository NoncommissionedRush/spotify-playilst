import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

#
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRET_URI = "http://example.com"


#  ------------------------------ log into Spotify --------------------------------------
scope = "playlist-modify-private"

sp = spotipy.Spotify( 
    auth_manager=SpotifyOAuth(
        SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRET_URI, scope=scope
    )
)

my_spotify_id = sp.current_user()["id"]


#  ----------------------------- create billboard url ----------------------------------
date = input("Write a date (YYYY-MM-DD) ")
url = f"https://www.billboard.com/charts/hot-100/{date}"
year = date[:4]



#  --------------------------- get songs from Billboard web -----------------------------
response = requests.get(url)
html_raw = response.text

soup = BeautifulSoup(html_raw, "html.parser")

elements = soup.select(".chart-list__element")
all_songs = []

for element in elements:
    artist = element.find(class_="chart-element__information__artist").getText()
    song_title = element.find(class_="chart-element__information__song").getText()
    all_songs.append(f"{artist}, {song_title}")



# -------------------------- get spotify song URIs from Spotify ---------------------------
song_uris = []

for song in all_songs:
    song_data = sp.search(song, limit=1, type="track")
    try:
        song_uri = song_data["tracks"]["items"][0]["uri"]
    except IndexError:
        pass
    else:
        song_uris.append(song_uri)


# ---------------------------- create new spotify playlist ----------------------------------
playlist = sp.user_playlist_create(my_spotify_id, f"Billboard top {date}", public=False)

playlist_id = playlist['id']


# --------------------------- add songs to new playlist -------------------------------------

sp.playlist_add_items(playlist_id, song_uris)

print("done")