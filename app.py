import streamlit as st
import toml
from spotipy import Spotify
from spotipy.cache_handler import CacheHandler
from spotipy.exceptions import SpotifyOauthError
from spotipy.oauth2 import SpotifyOAuth


class StreamlitCacheHandler(CacheHandler):
    def __init__(self):
        self.session_id = st.session_state.get("session_id")

    def get_cached_token(self):
        return st.session_state.get("spotipy_token")

    def save_token_to_cache(self, token_info):
        st.session_state["spotipy_token"] = token_info


def get_auth_manager():
    """
    Returns a spotipy.oauth2.SpotifyOAuth object.
    """
    return SpotifyOAuth(client_id=st.secrets["spotify"]["SPOTIFY_CLIENT_ID"],
                        client_secret=st.secrets["spotify"]["SPOTIFY_CLIENT_SECRET"],
                        redirect_uri=st.secrets["spotify"]["SPOTIFY_REDIRECT_URI"],
                        scope='user-top-read',
                        cache_handler=StreamlitCacheHandler()
                        )


def main():
    st.title("Spotify Playlists")
    sp = Spotify(auth_manager=get_auth_manager())
    if "spotipy_token" in st.session_state:
        playlists = sp.current_user_playlists()["items"]
        for index, playlist in enumerate(playlists):
            st.write(f"{index + 1}: "
                     f"[{playlist['name']}](https://open.spotify.com/playlist/{playlist['id']})")
    else:
        if st.button("Log in"):
            # prevents a new tab from being opened
            st.markdown(f'<meta http-equiv="refresh" content="0; '
                        f'url={sp.auth_manager.get_authorize_url()}"/>')


def callback():
    code = st.query_params.get("code")
    if code:
        try:
            token_info = get_auth_manager().get_access_token(code)
        except SpotifyOauthError:
            pass
    del st.query_params["code"]
    main()


if __name__ == "__main__":
    if st.query_params.get("code"):
        callback()
    else:
        main()
