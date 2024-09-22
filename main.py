import os
import base64
from requests import post
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import streamlit as st


CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = 'http://localhost:5000'

# Initialize spotipy client to interact with 
# Spotify API
sp = spotipy.Spotify (
    auth_manager=SpotifyOAuth(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        redirect_uri = REDIRECT_URI,
        scope = 'user-top-read' # only request top songs
    )
)

st.set_page_config(page_title = 'Spotify Song Analysis', page_icon = 'musical_note:')
st.title('Analysis for Top Songs')
st.write('Discover your Spotify listening habits!')

top_tracks = sp.current_user_top_tracks(limit = 10, time_range = 'short_term')
track_ids = [track['id'] for track in top_tracks['items']]
audio_features = sp.audio_features(track_ids) # returns audio features for each track

# Intialize a dataframe of audio features
df = pd.DataFrame(audio_features)
df['track_name'] = [track['name'] for track in top_tracks['items']]
df = df[['track_name', 'danceability', 'energy', 'valence']]
df.set_index('track_name', inplace = True)

#Creates chart
st.subheader('Audio Features for Top Tracks')
st.bar_chart(df, height = 500)