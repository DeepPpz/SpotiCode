import random, string
# Django
from django.contrib import admin
# Project
from spoticode.playlists.models import Playlist, SongPlaylistRelation
# Other 
from django_admin_listfilter_dropdown.filters import DropdownFilter


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('playlist_name', 'songs_local', 'songs_spotify', 'playlist_link', 'notes')
    search_fields = ('playlist_name', 'notes')
    
    def get_exclude(self, request, obj=None):
        if obj is None:
            return ['playlist_id',]
        return []
    
    def save_model(self, request, obj, form, change):
        if not obj.playlist_id:            
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            while Playlist.objects.filter(playlist_id=f'PL-{random_part}').exists():
                random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            obj.playlist_id = 'PL-' + random_part
        super().save_model(request, obj, form, change)


@admin.register(SongPlaylistRelation)
class SongPlaylistRelationAdmin(admin.ModelAdmin):
    list_display = ('playlist', 'song')
    search_fields = ('playlist_id__playlist_name', 'song_id__song_title',)
    list_filter = (
        ('playlist_id__playlist_name', DropdownFilter),
    )
    
    def playlist(self, obj):
        return obj.playlist_id.playlist_name if obj.playlist_id.playlist_name else ''
    
    def song(self, obj):
        return str(obj.song_id) if obj.song_id else ''
    
    def get_exclude(self, request, obj=None):
        if obj is None:
            return ['id',]
        return []

    def save_model(self, request, obj, form, change):
        if not obj.relation_id:
            random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
            while SongPlaylistRelation.objects.filter(relation_id=random_part).exists():
                random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
            obj.relation_id = random_part
        super().save_model(request, obj, form, change)
