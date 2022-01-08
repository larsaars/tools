import os
import spotipy
from spotipy import SpotifyOAuth

# read the credentials
with open('spotify_secrets.txt', 'r') as file:
    content = file.read().splitlines()
    client_id = content[0]
    client_secret = content[1]

# set as env variables
os.environ['SPOTIPY_CLIENT_ID'] = client_id
os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888/callback'

# login
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='playlist-read-private')) 
