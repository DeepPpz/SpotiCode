from datetime import datetime
#Django
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
# Project
from spoticode.songs.models import Song, PendingSong
from spoticode.playlists.models import SongPlaylistRelation
from spoticode.artists.models import Artist
from spoticode.albums.models import Album
from spoticode.songs.forms import CreateSongForm, EditSongForm, AddSongToPlaylistForm, CreatePendingSongForm, EditPendingSongForm
from spoticode.web.access_validators import custom_login_required, can_create_or_update, can_delete, can_read, is_staff
from spoticode.web.access_checkers import can_create_checker, can_edit_checker, can_delete_checker


# Songs
@custom_login_required
@can_read
def show_all_songs(request):
    songs = Song.objects.all()
    query = request.GET.get('query')
    
    if query:
        songs = Song.objects.filter(song_title__icontains=query) | \
            Song.objects.filter(main_artist__artist_name__icontains=query) | \
                Song.objects.filter(feat_artist__icontains=query) | \
                    Song.objects.filter(main_artist__other_names__icontains=query)
    
    songs = songs.order_by('main_artist__artist_name', 'song_title')
    
    paginator = Paginator(songs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'curr_year': datetime.now().year,
        'songs': songs,
        'total_songs': songs.count(),
        'page_obj': page_obj,
        'can_create_check': can_create_checker(request.user),
    }
    
    return render(request, 'songs/songs-all.html', context)


@custom_login_required
@can_read
def show_details_song(request, id):
    song = get_object_or_404(Song, song_id=id)
    album_name = song.album_id.album_name if song.album_id else '--single--'
    song_playlists = SongPlaylistRelation.objects.filter(song_id=id)
    playlists = [playlist.playlist_id.playlist_name for playlist in song_playlists] if song_playlists.exists() else '--none--'
    
    if playlists != '--none--':
        playlists = ', '.join(playlists)
    
    context = {
        'curr_year': datetime.now().year,
        'song': song,
        'album_name': album_name,
        'playlists': playlists,
        'can_edit_check': can_edit_checker(request.user),
        'can_delete_check': can_delete_checker(request.user),
    }
    
    return render(request, 'songs/song-details.html', context)


@custom_login_required
@can_create_or_update
def create_song(request):
    form = CreateSongForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        
        spotify_link = form.cleaned_data['spotify_link']
        if spotify_link and '?si=' in spotify_link:
            spotify_link = spotify_link.split('?si=')[0]
            form.cleaned_data['spotify_link'] = spotify_link
        
        song = form.save()
        return redirect('song_details', id=song.song_id)
    
    context = {
        'curr_year': datetime.now().year,
        'form': form,
    }
    
    return render(request, 'songs/song-create.html', context)


@custom_login_required
@can_create_or_update
def add_song_to_playlist(request, id):
    song = get_object_or_404(Song, song_id=id)
    
    if request.method == 'POST':
        form = AddSongToPlaylistForm(request.POST, song_id=id)
        if form.is_valid():
            playlist = form.cleaned_data['playlist']
            
            SongPlaylistRelation.objects.create(playlist_id=playlist, song_id=song)
            
            return redirect('song_details', id=song.song_id)
    else:
        form = AddSongToPlaylistForm(song_id=id)
    
    context = {
        'curr_year': datetime.now().year,
        'form': form,
        'song': song,
    }
    
    return render(request, 'songs/song-add-to-playlist.html', context)


@custom_login_required
@can_create_or_update
def edit_song(request, id):
    song = get_object_or_404(Song, song_id=id)
    form = EditSongForm(request.POST or None, instance=song)
    
    artist = song.main_artist
    various_artists = Artist.objects.filter(artist_name="Various Artists").first()
    album_queryset = Album.objects.filter(Q(album_artist=artist) | Q(album_artist=various_artists)).order_by('album_artist__artist_name', 'album_name')
    
    if request.method == 'POST' and form.is_valid():
        
        spotify_link = form.cleaned_data['spotify_link']
        if spotify_link and '?si=' in spotify_link:
            spotify_link = spotify_link.split('?si=')[0]
            song.spotify_link = spotify_link
        
        form.save()
        return redirect('song_details', id=song.song_id)
    
    else:
        form = EditSongForm(request.POST or None, instance=song)
        form.fields['album_id'].queryset = album_queryset
    
    context = {
        'curr_year': datetime.now().year,
        'song': song,
        'form': form,
    }
    
    return render(request, 'songs/song-edit.html', context)
    

@custom_login_required
@can_delete
def delete_song(request, id):
    song = get_object_or_404(Song, song_id=id)
    
    if request.method == 'POST':
        song.delete()
        return redirect('songs_all')

    context = {
        'curr_year': datetime.now().year,
        'song': song,
    }
    
    return render(request, 'songs/song-delete.html', context)



# Pending Songs
@custom_login_required
@can_read
def show_all_pending_songs(request):
    pending_songs = PendingSong.objects.all()
    query = request.GET.get('query')
    added_songs = PendingSong.objects.filter(is_added=True).exists()
    
    if query:
        pending_songs = PendingSong.objects.filter(song_title__icontains=query) | \
            PendingSong.objects.filter(main_artist__icontains=query) | \
                PendingSong.objects.filter(feat_artist__icontains=query)
    
    pending_songs = pending_songs.order_by('main_artist', 'song_title')
    
    paginator = Paginator(pending_songs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'curr_year': datetime.now().year,
        'pending_songs': pending_songs,
        'total_pending_songs': pending_songs.count(),
        'page_obj': page_obj,
        'can_create_check': can_create_checker(request.user),
        'is_staff_check': request.user.is_staff,
        'added_songs': added_songs,
    }
    
    return render(request, 'songs/pending_songs/pending-songs-all.html', context)


@custom_login_required
@can_read
def show_details_pending_song(request, id):
    pending_song = get_object_or_404(PendingSong, pending_id=id)
    
    context = {
        'curr_year': datetime.now().year,
        'pending_song': pending_song,
        'can_edit_check': can_edit_checker(request.user),
        'can_delete_check': can_delete_checker(request.user),
    }
    
    return render(request, 'songs/pending_songs/pending-song-details.html', context)


@custom_login_required
@can_create_or_update
def create_pending_song(request):
    form = CreatePendingSongForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        pending_song = form.save()
        return redirect('pending_song_details', id=pending_song.pending_id)
    
    context = {
        'curr_year': datetime.now().year,
        'form': form,
    }
    
    return render(request, 'songs/pending_songs/pending-song-create.html', context)


@custom_login_required
@can_create_or_update
def edit_pending_song(request, id):
    pending_song = get_object_or_404(PendingSong, pending_id=id)
    form = EditPendingSongForm(request.POST or None, instance=pending_song)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('pending_song_details', id=pending_song.pending_id)
    
    context = {
        'curr_year': datetime.now().year,
        'pending_song': pending_song,
        'form': form,
    }
    
    return render(request, 'songs/pending_songs/pending-song-edit.html', context)


@custom_login_required
@can_delete
def delete_pending_song(request, id):
    pending_song = get_object_or_404(PendingSong, pending_id=id)
    
    if request.method == 'POST':
        pending_song.delete()
        return redirect('pending_songs_all')

    context = {
        'curr_year': datetime.now().year,
        'pending_song': pending_song,
    }
    
    return render(request, 'songs/pending_songs/pending-song-delete.html', context)


@custom_login_required
@is_staff
def delete_added_pending_songs(request):
    pending_songs = PendingSong.objects.filter(is_added=True)
    total_pendings_songs = pending_songs.count()
    
    if request.method == 'POST' and pending_songs:
        for song in pending_songs:
            song.delete()
        
        return redirect('pending_songs_all')
        
    context = {
        'curr_year': datetime.now().year,
        'pending_songs': pending_songs,
        'total_pending_songs': total_pendings_songs,
    }
    
    return render(request, 'songs/pending_songs/pending-song-multiple-delete.html', context)
