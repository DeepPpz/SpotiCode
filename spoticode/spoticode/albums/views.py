from datetime import datetime
# Django
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
# Project
from spoticode.albums.models import Album, AlbumLink, AlbumTrack
from spoticode.albums.forms import CreateAlbumForm, EditAlbumForm, EditAlbumLinkForm, CreateAlbumTrackForm, EditAlbumTrackForm
from spoticode.web.access_validators import custom_login_required, can_create_or_update, can_delete, can_read
from spoticode.web.access_checkers import can_create_checker, can_edit_checker, can_delete_checker


# Albums
@custom_login_required
@can_read
def show_all_albums(request):
    albums = Album.objects.all()
    query = request.GET.get('query')
    
    if query:
        albums = Album.objects.filter(album_name__icontains=query) | \
            Album.objects.filter(album_artist__artist_name__icontains=query) | \
                Album.objects.filter(album_artist__other_names__icontains=query)
    
    albums = albums.order_by('album_artist__artist_name', 'album_name')
    
    paginator = Paginator(albums, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'curr_year': datetime.now().year,
        'albums': albums,
        'total_albums': albums.count(),
        'page_obj': page_obj,
        'can_create_check': can_create_checker(request.user),
    }
    
    return render(request, 'albums/albums-all.html', context)


@custom_login_required
@can_read
def show_details_album(request, id):
    album = get_object_or_404(Album, album_id=id)
    album_links = get_object_or_404(AlbumLink, album_id=id)
    album_tracks = AlbumTrack.objects.filter(album_id=id)
    
    context = {
        'curr_year': datetime.now().year,
        'album': album,
        'album_links': album_links,
        'album_tracks': album_tracks,
        'can_create_check': can_create_checker(request.user),
        'can_edit_check': can_edit_checker(request.user),
        'can_delete_check': can_delete_checker(request.user),
    }
    
    return render(request, 'albums/album-details.html', context)


@custom_login_required
@can_create_or_update
def create_album(request):
    form = CreateAlbumForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        album = form.save()
        return redirect('album_details', id=album.album_id)

    context = {
        'curr_year': datetime.now().year,
        'form': form,
    }

    return render(request, 'albums/album-create.html', context)


@custom_login_required
@can_create_or_update
def edit_album_info(request, id):
    album = get_object_or_404(Album, album_id=id)
    form = EditAlbumForm(request.POST or None, instance=album)
    
    if request.method == 'POST' and form.is_valid():
        album = form.save()
        return redirect('album_details', id=album.album_id)
    
    context = {
        'curr_year': datetime.now().year,
        'album': album,
        'form': form,
    }
    
    return render(request, 'albums/album-info-edit.html', context)


@custom_login_required
@can_create_or_update
def edit_album_links(request, id):
    album = get_object_or_404(Album, album_id=id)
    album_links = get_object_or_404(AlbumLink, album_id=id)
    form = EditAlbumLinkForm(request.POST or None, instance=album_links)
    
    if request.method == 'POST' and form.is_valid():
        
        spotify_link = form.cleaned_data['spotify_link']
        if spotify_link and '?si=' in spotify_link:
            spotify_link = spotify_link.split('?si=')[0]
            album_links.spotify_link = spotify_link
        
        wiki_curid = form.cleaned_data['wiki_curid']
        if wiki_curid:
            wiki_link = f'https://en.wikipedia.org/?curid={wiki_curid}'
            album_links.wikipedia_link = wiki_link
        elif not wiki_curid:
            album_links.wikipedia_link = None
        
        album_links = form.save()
        return redirect('album_details', id=album.album_id)
    
    context = {
        'curr_year': datetime.now().year,
        'album': album,
        'album_links': album_links,
        'form': form,
    }
    
    return render(request, 'albums/album-links-edit.html', context)


@custom_login_required
@can_delete
def delete_album(request, id):
    album = get_object_or_404(Album, album_id=id)
    
    if request.method == 'POST':
        album.delete()
        return redirect('albums_all')

    context = {
        'curr_year': datetime.now().year,
        'album': album,
    }
    
    return render(request, 'albums/album-delete.html', context)



# Album Tracks
@custom_login_required
@can_create_or_update
def create_album_track(request, id):
    album = get_object_or_404(Album, album_id=id)
    form = CreateAlbumTrackForm(request.POST or None, album_id=album.album_id)
    
    if request.method == 'POST' and form.is_valid():
        album_track = form.save(commit=False)
        album_track.album_id = album
        album_track.save()
        return redirect('album_details', id=album.album_id)

    context = {
        'curr_year': datetime.now().year,
        'form': form,
        'album': album,
    }

    return render(request, 'albums/tracks/album-track-create.html', context)


@custom_login_required
@can_create_or_update
def edit_album_track(request, id, tr_id):
    album = get_object_or_404(Album, album_id=id)
    album_track = get_object_or_404(AlbumTrack, track_id=tr_id)
    form = EditAlbumTrackForm(request.POST or None, instance=album_track)
    
    if request.method == 'POST' and form.is_valid():
        album_track = form.save()
        return redirect('album_details', id=album.album_id)
    
    context = {
        'curr_year': datetime.now().year,
        'album': album,
        'album_track': album_track,
        'form': form,
    }
    
    return render(request, 'albums/tracks/album-track-edit.html', context)


@custom_login_required
@can_delete
def delete_album_track(request, id, tr_id):
    album = get_object_or_404(Album, album_id=id)
    album_track = get_object_or_404(AlbumTrack, track_id=tr_id)
    
    if request.method == 'POST':
        album_track.delete()
        return redirect('album_details', id=album.album_id)

    context = {
        'curr_year': datetime.now().year,
        'album': album,
        'album_track': album_track,
    }
    
    return render(request, 'albums/tracks/album-track-delete.html', context)
