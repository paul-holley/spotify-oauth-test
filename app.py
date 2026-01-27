import streamlit as st
from spotipy.oauth2 import SpotifyOAuth
import spotipy

st.set_page_config(page_title="Spotify OAuth Test")

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