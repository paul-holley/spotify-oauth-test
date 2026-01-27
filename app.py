import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

st.set_page_config(page_title="Spotify OAuth Test")

# --- Initialize session state ---
if "token_info" not in st.session_state:
    st.session_state.token_info = None

# --- Create OAuth object ---
oauth = SpotifyOAuth(
    client_id=st.secrets["spotify"]["SPOTIFY_CLIENT_ID"],
    client_secret=st.secrets["spotify"]["SPOTIFY_CLIENT_SECRET"],
    redirect_uri=st.secrets["spotify"]["SPOTIFY_REDIRECT_URI"],
    scope="user-top-read",
    cache_path=None,  # prevents shared logins
    show_dialog=True,
)

# --- Handle redirect back from Spotify ---
query_params = st.query_params

if "code" in query_params and st.session_state.token_info is None:
    code = query_params["code"]
    token_info = oauth.get_access_token(code, as_dict=True)
    st.session_state.token_info = token_info

    st.query_params.clear()
    st.rerun()

# --- Force login ---
if st.session_state.token_info is None:
    auth_url = oauth.get_authorize_url()
    st.markdown("## 🎧 Spotify Login Required")
    st.markdown(f"[Click here to log in with Spotify]({auth_url})")
    st.stop()

# --- Refresh token if needed ---
if oauth.is_token_expired(st.session_state.token_info):
    st.session_state.token_info = oauth.refresh_access_token(
        st.session_state.token_info["refresh_token"]
    )

# --- Logged in ---
sp = spotipy.Spotify(auth=st.session_state.token_info["access_token"])
user = sp.current_user()

st.success("✅ Logged in!")
st.write("Display name:", user["display_name"])
st.write("User ID:", user["id"])