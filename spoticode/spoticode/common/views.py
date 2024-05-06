from datetime import datetime
# Django
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
# Project
from spoticode.common.models import MusicGroup, Genre
from spoticode.common.forms import CreateMusicGroupForm, EditMusicGroupForm, CreateGenreForm, EditGenreForm
from spoticode.web.access_validators import custom_login_required, can_create_or_update, can_read, is_staff
from spoticode.web.access_checkers import can_create_checker, can_edit_checker


# Music Groups
@custom_login_required
@can_read
def show_all_music_groups(request):
    music_groups = MusicGroup.objects.all()
    query = request.GET.get('query')
    
    if query:
        music_groups = MusicGroup.objects.filter(group_name__icontains=query)
    
    music_groups = music_groups.order_by('group_name')
    
    paginator = Paginator(music_groups, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'curr_year': datetime.now().year,
        'music_groups': music_groups,
        'total_groups': music_groups.count(),
        'page_obj': page_obj,
        'can_create_check': can_create_checker(request.user),
    }
    
    return render(request, 'common/music_groups/music-groups-all.html', context)


@custom_login_required
@can_read
def show_details_music_group(request, id):
    music_group = get_object_or_404(MusicGroup, id=id)

    context = {
        'curr_year': datetime.now().year,
        'music_group': music_group,
        'can_edit_check': can_edit_checker(request.user),
        'is_staff_check': request.user.is_staff,
    }
    
    return render(request, 'common/music_groups/music-group-details.html', context)


@custom_login_required
@can_create_or_update
def create_music_group(request):
    form = CreateMusicGroupForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        music_group = form.save()
        return redirect('music_group_details', id=music_group.id)
    
    context = {
        'curr_year': datetime.now().year,
        'form': form,
    }
    
    return render(request, 'common/music_groups/music-group-create.html', context)


@custom_login_required
@can_create_or_update
def edit_music_group(request, id):
    music_group = get_object_or_404(MusicGroup, id=id)
    form = EditMusicGroupForm(request.POST or None, instance=music_group)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('music_group_details', id=id)
    
    context = {
        'curr_year': datetime.now().year,
        'music_group': music_group,
        'form': form,
        'id': id,
    }
    
    return render(request, 'common/music_groups/music-group-edit.html', context)


@custom_login_required
@is_staff
def delete_music_group(request, id):
    music_group = get_object_or_404(MusicGroup, id=id)
    
    if request.method == 'POST':
        music_group.delete()
        return redirect('music_groups_all')

    context = {
        'curr_year': datetime.now().year,
        'music_group': music_group,
    }
    
    return render(request, 'common/music_groups/music-group-delete.html', context)



# Genres
@custom_login_required
@can_read
def show_all_genres(request):
    genres = Genre.objects.all()
    query = request.GET.get('query')
    
    if query:
        genres = Genre.objects.filter(genre_name__icontains=query)
    
    genres = genres.order_by('genre_name')
    
    paginator = Paginator(genres, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'curr_year': datetime.now().year,
        'genres': genres,
        'total_genres': genres.count(),
        'page_obj': page_obj,
        'can_create_check': can_create_checker(request.user),
    }
    
    return render(request, 'common/genres/genres-all.html', context)


@custom_login_required
@can_read
def show_details_genre(request, id):
    genre = get_object_or_404(Genre, id=id)
    
    context = {
        'curr_year': datetime.now().year,
        'genre': genre,
        'can_edit_check': can_edit_checker(request.user),
        'is_staff_check': request.user.is_staff,
    }
    
    return render(request, 'common/genres/genre-details.html', context)


@custom_login_required
@can_create_or_update
def create_genre(request):
    form = CreateGenreForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        genre = form.save()
        return redirect('genre_details', id=genre.id)
    
    context = {
        'curr_year': datetime.now().year,
        'form': form,
    }
    
    return render(request, 'common/genres/genre-create.html', context)


@custom_login_required
@can_create_or_update
def edit_genre(request, id):
    genre = get_object_or_404(Genre, id=id)
    form = EditGenreForm(request.POST or None, instance=genre)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('genre_details', id=id)
    
    context = {
        'curr_year': datetime.now().year,
        'genre': genre,
        'form': form,
        'id': id,
    }
    
    return render(request, 'common/genres/genre-edit.html', context)


@custom_login_required
@is_staff
def delete_genre(request, id):
    genre = get_object_or_404(Genre, id=id)
    
    if request.method == 'POST':
        genre.delete()
        return redirect('genres_all')

    context = {
        'curr_year': datetime.now().year,
        'genre': genre,
    }
    
    return render(request, 'common/genres/genre-delete.html', context)
