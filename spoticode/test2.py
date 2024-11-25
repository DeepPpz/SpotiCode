from datetime import datetime, time
import os
# Django
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
# Project
from spoticode.songs.models import Song
from spoticode.playlists.models import Playlist, SongPlaylistRelation
from spoticode.playlists.forms import CreatePlaylistForm, EditPlaylistForm, SongsSearchForm
from spoticode.web.access_validators import custom_login_required, can_create_or_update, can_delete, can_read
from spoticode.web.access_checkers import can_create_checker, can_edit_checker, can_delete_checker
# Spotify API
import spotipy
from spotipy.oauth2 import SpotifyOAuth


@custom_login_required
@can_create_or_update
def mass_add_songs(request, id):
    if request.method == 'POST':
        spotify_log = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get('CLIENT_ID'),
                                                    client_secret=os.environ.get('CLIENT_SECRET'),
                                                    redirect_uri="http://localhost:8081",
                                                    scope="playlist-modify-public"))
        
        selected_songs = request.POST.getlist('songs')
        playlist = get_object_or_404(Playlist, playlist_id=id)
        spotify_playlist = spotify_log.user_playlist_create(spotify_log.me()["id"], playlist.playlist_name, public=True)
        playlist_id = spotify_playlist["id"]
        playlist_url = spotify_playlist['external_urls']['spotify']
        
        max_tracks = 100  # Maximum number of tracks allowed per request
        partly_track_links = [selected_songs[i:i+max_tracks] for i in range(0, len(selected_songs), max_tracks)]
        
        for curr_piece in partly_track_links:
            # Add song to Spotify
            track_ids = [link.split("/")[-1].split("?")[0] for link in curr_piece if link]
            spotify_log.playlist_add_items(playlist_id, track_ids)
            
            # Add song to mapping table
            song = Song.objects.get(song_id=song_id)
            if not SongPlaylistRelation.objects.filter(playlist_id=playlist, song_id=song).exists():
                SongPlaylistRelation.objects.create(playlist_id=playlist, song_id=song)
            
            time.sleep(2)
        
    return redirect('playlist_songs_all', id=playlist.playlist_id)