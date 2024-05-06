from datetime import datetime
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


# Playlists
@custom_login_required
@can_read
def show_all_playlists(request):
    playlists = Playlist.objects.all()
    query = request.GET.get('query')
    
    if query:
        playlists = Playlist.objects.filter(playlist_name__icontains=query) | \
            Playlist.objects.filter(notes__icontains=query)
    
    paginator = Paginator(playlists, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'curr_year': datetime.now().year,
        'playlists': playlists,
        'total_playlists': playlists.count(),
        'page_obj': page_obj,
        'can_create_check': can_create_checker(request.user),
    }
    
    return render(request, 'playlists/playlists-all.html', context)


@custom_login_required
@can_read
def show_details_playlist(request, id):
    playlist = get_object_or_404(Playlist, playlist_id=id)
    songs = SongPlaylistRelation.objects.filter(playlist_id=playlist.playlist_id)
    songs_count = songs.count()
    
    context = {
        'curr_year': datetime.now().year,
        'playlist': playlist,
        'songs_count': songs_count,
        'can_edit_check': can_edit_checker(request.user),
        'can_delete_check': can_delete_checker(request.user),
    }
    
    return render(request, 'playlists/playlist-details.html', context)


@custom_login_required
@can_create_or_update
def create_playlist(request):
    form = CreatePlaylistForm(request.POST or None, request.FILES)
    
    if request.method == 'POST' and form.is_valid():
        
        playlist_link = form.cleaned_data['playlist_link']
        if playlist_link and '?si=' in playlist_link:
            playlist_link = playlist_link.split('?si=')[0]
            form.cleaned_data['playlist_link'] = playlist_link
        
        playlist = form.save()
        return redirect('playlist_details', id=playlist.playlist_id)

    context = {
        'curr_year': datetime.now().year,
        'form': form,
    }

    return render(request, 'playlists/playlist-create.html', context)


@custom_login_required
@can_create_or_update
def edit_playlist_info(request, id):
    playlist = get_object_or_404(Playlist, playlist_id=id)
    
    if request.method == 'POST':
        form = EditPlaylistForm(request.POST, request.FILES, instance=playlist)
        
        if form.is_valid():
            playlist_link = form.cleaned_data['playlist_link']
            if playlist_link and '?si=' in playlist_link:
                playlist_link = playlist_link.split('?si=')[0]
                playlist.playlist_link = playlist_link
            
            form.save()
            return redirect('playlist_details', id=id)
    
    else:
        form = EditPlaylistForm(instance=playlist)
    
    context = {
        'curr_year': datetime.now().year,
        'playlist': playlist,
        'form': form,
        'id': id,
    }
    
    return render(request, 'playlists/playlist-info-edit.html', context)


@custom_login_required
@can_delete
def delete_playlist(request, id):
    playlist = get_object_or_404(Playlist, playlist_id=id)
    
    if request.method == 'POST':
        playlist.delete()
        return redirect('playlists_all')

    context = {
        'curr_year': datetime.now().year,
        'playlist': playlist,
    }
    
    return render(request, 'playlists/playlist-delete.html', context)



# Song-Playlist Relations
@custom_login_required
@can_read
def show_all_playlist_songs(request, id):
    playlist = get_object_or_404(Playlist, playlist_id=id)
    all_songs = SongPlaylistRelation.objects.filter(playlist_id=id)
    query = request.GET.get('query')
    
    if query:
        all_songs = all_songs.filter(song_id__song_title__icontains=query) | \
            all_songs.filter(song_id__main_artist__artist_name__icontains=query) | \
                all_songs.filter(song_id__feat_artist__icontains=query)
    
    all_songs = all_songs.order_by('song_id__main_artist__artist_name', 'song_id__song_title')
    
    paginator = Paginator(all_songs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'curr_year': datetime.now().year,
        'playlist': playlist,
        'all_songs': all_songs,
        'total_songs': all_songs.count(),
        'page_obj': page_obj,
        'can_create_check': can_create_checker(request.user),
        'can_delete_check': can_delete_checker(request.user),
    }
    
    return render(request, 'playlists/song_playlist_relations/playlist-songs-all.html', context)


@custom_login_required
@can_create_or_update
def select_songs_for_mass_add(request, id):
    playlist = get_object_or_404(Playlist, playlist_id=id)
    form = SongsSearchForm(request.GET)
    songs = Song.objects.all()
    
    if form.is_valid():
        artist = form.cleaned_data.get('artist')
        from_year = form.cleaned_data.get('from_year')
        to_year = form.cleaned_data.get('to_year')
        genre = form.cleaned_data.get('genre')
        group = form.cleaned_data.get('group')

        if artist:
            songs = songs.filter(main_artist__artist_name__icontains=artist) | \
                songs.filter(feat_artist__icontains=artist)
        if from_year:
            songs = songs.filter(song_year__gte=from_year)
        if to_year:
            songs = songs.filter(song_year__lte=to_year)
        if genre:
            songs = songs.filter(genre__genre_name__icontains=genre)
        if group:
            songs = songs.filter(group__group_name__icontains=group)
      
    total_songs = songs.count()
    
    context = {
        'curr_year': datetime.now().year,
        'playlist': playlist,
        'songs': songs,
        'total_songs': total_songs,
        'form': form,
        'can_create_check': can_create_checker(request.user),
    }

    return render(request, 'playlists/song_playlist_relations/playlist-songs-preview-mass-add.html', context)


@custom_login_required
@can_create_or_update
def mass_add_songs(request, id):
    if request.method == 'POST':
        selected_songs = request.POST.getlist('songs')
        playlist = get_object_or_404(Playlist, playlist_id=id)

        for song_id in selected_songs:
            song = Song.objects.get(song_id=song_id)
            
            if not SongPlaylistRelation.objects.filter(playlist_id=playlist, song_id=song).exists():
                SongPlaylistRelation.objects.create(playlist_id=playlist, song_id=song)


    return redirect('playlist_songs_all', id=playlist.playlist_id)


@custom_login_required
@can_delete
def delete_song_from_playlist(request, id, s_id):
    playlist = get_object_or_404(Playlist, playlist_id=id)
    song = get_object_or_404(SongPlaylistRelation, playlist_id=id, song_id=s_id)
    
    if request.method == 'POST':
        song.delete()
    
    return redirect('playlist_songs_all', id=playlist.playlist_id)
