import spotipy
from spotipy.oauth2 import SpotifyOAuth
import psycopg2
import config
import time


def generate_playlist_with_links(spotify, playlist_name, track_links):
    track_links = [row[0] for row in cursor.fetchall()]

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config.client_id,
                                                    client_secret=config.client_secret,
                                                    redirect_uri="http://localhost:8081",
                                                    scope="playlist-modify-public"))
    
    playlist = spotify.user_playlist_create(spotify.me()["id"], playlist_name, public=True)
    playlist_id = playlist["id"]

    max_tracks = 100  # Maximum number of tracks allowed per request
    partly_track_links = [track_links[i:i+max_tracks] for i in range(0, len(track_links), max_tracks)]

    for curr_piece in partly_track_links:
        track_ids = [link.split("/")[-1].split("?")[0] for link in curr_piece if link]

        spotify.playlist_add_items(playlist_id, track_ids)
        print(f"Added {len(track_ids)} tracks to the playlist.")
        
        time.sleep(2)

    print(f"Playlist '{playlist_name}' with {len(track_links)} tracks created.")


try:
    connection = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password
    )
    cursor = connection.cursor()
    
    playlist_name = "Test Playlist"
    cursor.execute("SELECT spotify_link FROM pop_table WHERE main_folder LIKE '2010%';")
    track_links = [row[0] for row in cursor.fetchall()]

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config.client_id,
                                                    client_secret=config.client_secret,
                                                    redirect_uri="http://localhost:8081",
                                                    scope="playlist-modify-public"))

    generate_playlist_with_links(sp, playlist_name, track_links)

except psycopg2.Error as e:
    print("Error: ", e)

finally:
    if connection:
        connection.close()
