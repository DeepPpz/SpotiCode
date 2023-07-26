import spotipy
from spotipy.oauth2 import SpotifyOAuth
import psycopg2

db_host = "localhost"
db_name = "spotify_db"
db_user = "postgres"
db_password = "******"
connection = None


def generate_playlist_with_links(spotify, playlist_name, track_links):
    playlist = spotify.user_playlist_create(spotify.me()["id"], playlist_name, public=False)
    playlist_id = playlist["id"]

    max_tracks = 100  # Maximum number of tracks allowed per request
    partly_track_links = [track_links[i:i+max_tracks] for i in range(0, len(track_links), max_tracks)]

    for curr_piece in partly_track_links:
        track_ids = [link.split("/")[-1].split("?")[0] for link in curr_piece if link]

        spotify.playlist_add_items(playlist_id, track_ids)
        print(f"Added {len(track_ids)} tracks to the playlist.")

    print(f"Playlist '{playlist_name}' with {len(track_links)} tracks created.")


def main():
    client_id = ""
    client_secret = ""

    playlist_name = "AI EDM Playlist"

    connection = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password
    )

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT spotify_link FROM all_pop_table WHERE main_folder LIKE '%EDM%';")
        track_links = [row[0] for row in cursor.fetchall()]

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                      client_secret=client_secret,
                                                      redirect_uri="http://localhost",
                                                      scope="playlist-modify-private"))

        generate_playlist_with_links(sp, playlist_name, track_links)

    except psycopg2.Error as e:
        print("Error: ", e)

    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    main()
