import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import CacheHandler

class StreamlitCacheHandler(CacheHandler):
    def __init__(self, session_key="token_info"):
        self.session_key = session_key

    def get_cached_token(self):
        return st.session_state.get(self.session_key)

    def save_token_to_cache(self, token_info):
        st.session_state[self.session_key] = token_info


st.set_page_config(page_title="Spotify OAuth Test")

# --- Create OAuth object ONCE ---

cache_handler = StreamlitCacheHandler()
oauth = SpotifyOAuth(
    client_id=st.secrets["spotify"]["SPOTIFY_CLIENT_ID"],
    client_secret=st.secrets["spotify"]["SPOTIFY_CLIENT_SECRET"],
    redirect_uri=st.secrets["spotify"]["SPOTIFY_REDIRECT_URI"],
    scope="user-top-read",
    cache_handler=cache_handler,      # important for multi-user apps
    show_dialog=True,
)

# --- Handle redirect ---
query_params = st.query_params

if "code" in query_params:
    oauth.get_access_token(query_params["code"], as_dict=True)
    st.query_params.clear()
    st.rerun()

# --- Require login ---
token = oauth.get_cached_token()

if not token:
    auth_url = oauth.get_authorize_url()
    st.markdown("## 🎧 Spotify Login Required")
    st.markdown(f"[Click here to log in with Spotify]({auth_url})")
    st.stop()

# --- Logged in (THIS is the key change) ---
sp = spotipy.Spotify(auth_manager=oauth)
user = sp.current_user()

st.success("✅ Logged in!")
st.write("Display name:", user["display_name"])
st.write("User ID:", user["id"])