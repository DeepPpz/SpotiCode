import spotipy
from spotipy.oauth2 import SpotifyOAuth
import psycopg2

db_host = "localhost"
db_name = "spotify_db"
db_user = "postgres"
db_password = "******"
connection = None


def generate_playlist_with_links(spotify, playlist_name, track_links):
    # Create an empty playlist
    playlist = spotify.user_playlist_create(spotify.me()["id"], playlist_name, public=False)
    playlist_id = playlist["id"]

    # Split the track links into smaller chunks
    chunk_size = 100  # Maximum number of tracks allowed per request
    track_link_chunks = [track_links[i:i+chunk_size] for i in range(0, len(track_links), chunk_size)]

    for track_links_chunk in track_link_chunks:
        # Get the track IDs from the track links (excluding None values)
        track_ids = [link.split("/")[-1].split("?")[0] for link in track_links_chunk if link]

        # Add the tracks to the playlist
        spotify.playlist_add_items(playlist_id, track_ids)
        print(f"Added {len(track_ids)} tracks to the playlist.")

    print(f"Playlist '{playlist_name}' with {len(track_links)} tracks created.")


def main():
    client_id = ""
    client_secret = ""

    playlist_name = "AI Generated Playlist"

    connection = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password
    )

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT spotify_link FROM all_pop_table;")
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
