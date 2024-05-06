import random, string
# Django
from django.contrib import admin
# Project
from spoticode.songs.models import Song, PendingSong
from spoticode.songs.admin_filters import SongsAlbumsNoAlbumsFilter, SongsLinksNoLinksFilter
from spoticode.songs.admin_actions import make_added, copy_to_songs_table
# Other
from django_admin_listfilter_dropdown.filters import DropdownFilter


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('song_id', 'song_title', 'artist', 'feat_artist', 'genre', 'song_year', 'group', 'album', 'spotify_link')
    search_fields = ('song_title', 'main_artist__artist_name', 'feat_artist', 'album_id__album_name')
    list_filter = (
        ('main_artist__artist_name', DropdownFilter),
        ('album_id__album_name', DropdownFilter),
        ('group__group_name', DropdownFilter),
        ('genre__genre_name', DropdownFilter),
        (SongsAlbumsNoAlbumsFilter), 
        (SongsLinksNoLinksFilter),
    )
    
    def artist(self, obj):
        return obj.main_artist.artist_name if obj.main_artist else None
    
    def genre(self, obj):
        return obj.genre.genre_name if obj.genre else '--unknown--'
    
    def group(self, obj):
        return obj.group.group_name if obj.group else None
    
    def album(self, obj):
        return obj.album_id.album_name if obj.album_id else '--single--'
    
    def get_exclude(self, request, obj=None):
        if obj is None:
            return ['song_id',]
        return []
    
    def save_model(self, request, obj, form, change):
        if not obj.song_id:
            artist_id = obj.main_artist.artist_id
            song_no = obj.main_artist.songs_count + 1
            obj.song_id = f'{artist_id}{song_no:03}'
        super().save_model(request, obj, form, change)


@admin.register(PendingSong)
class PendingSongAdmin(admin.ModelAdmin):
    list_display = ('song_title', 'main_artist', 'feat_artist', 'group', 'is_added', 'new_artist')
    search_fields = ('song_title', 'main_artist', 'feat_artist')
    list_filter = (
        ('to_group__group_name', DropdownFilter),
        ('is_added'),
        ('new_artist'),
    )
    
    actions = (make_added, copy_to_songs_table)
    
    def group(self, obj):
        return obj.to_group.group_name if obj.to_group else None
    
    def get_exclude(self, request, obj=None):
        if obj is None:
            return ['pending_id', 'is_added', 'new_artist']
        return []

    def save_model(self, request, obj, form, change):
        if not obj.pending_id:
            random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
            while PendingSong.objects.filter(pending_id=random_part).exists():
                random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
            obj.pending_id = random_part
        super().save_model(request, obj, form, change)
