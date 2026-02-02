import streamlit as st
from spotipy.oauth2 import SpotifyOAuth
import spotipy

st.set_page_config(page_title="Spotify OAuth Test")

client_id = st.secrets["spotify"]["SPOTIFY_CLIENT_ID"]
client_secret = st.secrets["spotify"]["SPOTIFY_CLIENT_SECRET"]
redirect_uri = st.secrets["spotify"]["SPOTIFY_REDIRECT_URI"]

# OAuth endpoints given in the Spotify API documentation
# https://developer.spotify.com/documentation/general/guides/authorization/code-flow/
authorization_base_url = "https://accounts.spotify.com/authorize"
token_url = "https://accounts.spotify.com/api/token"
# https://developer.spotify.com/documentation/general/guides/authorization/scopes/
scope = [
    "user-top-read"
]

from requests_oauthlib import OAuth2Session
spotify = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)

# Redirect user to Spotify for authorization
authorization_url, state = spotify.authorization_url(authorization_base_url)
st.link_button("authenticate with spotify", authorization_url)

# Get the authorization verifier code from the callback url
redirect_response = input('\n\nPaste the full redirect URL here: ')

from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth(client_id, client_secret)

# Fetch the access token
token = spotify.fetch_token(token_url, auth=auth,
                            authorization_response=redirect_response)

print(token)

# Fetch a protected resource, i.e. user profile
r = spotify.get('https://api.spotify.com/v1/me')
print(r.content)




'''
# --- Session state ---
if "token_info" not in st.session_state:
    st.session_state.token_info = None

# --- Create OAuth object ONCE ---
if "oauth" not in st.session_state:
    st.session_state.oauth = SpotifyOAuth(
        client_id=st.secrets["spotify"]["SPOTIFY_CLIENT_ID"],
        client_secret=st.secrets["spotify"]["SPOTIFY_CLIENT_SECRET"],
        redirect_uri=st.secrets["spotify"]["SPOTIFY_REDIRECT_URI"],
        scope="user-top-read",
        cache_path=None,  # avoid shared token issues
        show_dialog=True
    )

oauth = st.session_state.oauth

# --- Handle redirect from Spotify ---
query_params = st.query_params

if "code" in query_params and st.session_state.token_info is None:
    code = query_params["code"][0]  # query_params returns a list
    token_info = oauth.get_access_token(code, as_dict=True)
    st.session_state.token_info = token_info

    # Clear query params so this block doesn't run again
    st.experimental_set_query_params()
    st.experimental_rerun()

# --- Require login ---
if st.session_state.token_info is None:
    auth_url = oauth.get_authorize_url()
    st.markdown("## 🎧 Spotify Login Required")
    st.markdown(f"[Click here to log in with Spotify]({auth_url})")
    st.stop()

# --- Logged in ---
sp = spotipy.Spotify(auth=st.session_state.token_info["access_token"])
user = sp.current_user()

st.success("✅ Logged in!")
st.write("Display name:", user["display_name"])
st.write("User ID:", user["id"])
'''