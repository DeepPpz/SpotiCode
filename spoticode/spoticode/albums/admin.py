import random, string
# Django
from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter
# Project
from spoticode.albums.models import Album, AlbumLink, AlbumTrack
from spoticode.albums.admin_filters import AlbumsReleaseDateFilter, AlbumLinksFilter, AvailableTracksFilter


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('album_id', 'release_date', 'artist', 'album_name', 'album_type')
    search_fields = ('album_artist__artist_name', 'album_artist__other_names', 'album_name')
    list_filter = (
        ('album_artist__artist_name', DropdownFilter),
        ('album_type', DropdownFilter),
        (AlbumsReleaseDateFilter),
    )
    
    def artist(self, obj):
        return obj.album_artist.artist_name if obj.album_artist else ''
    
    def get_exclude(self, request, obj=None):
        if obj is None:
            return ['album_id']
        return []
    
    def save_model(self, request, obj, form, change):
        artist_id = obj.album_artist.artist_id
        if not obj.album_id or obj.album_id.split("-A")[0] != artist_id:
            album_no = obj.album_artist.albums_count + 1
            obj.album_id = f'{artist_id}-A{album_no:02}'
        super().save_model(request, obj, form, change)


@admin.register(AlbumLink)
class AlbumLinkAdmin(admin.ModelAdmin):
    list_display = ('album', 'spotify_link', 'wikipedia_link', 'rateyourmusic_link')
    search_fields = ('album_id__album_name', 'album_id__album_artist__artist_name')
    list_filter = (
        (AlbumLinksFilter),
    )
    
    def album(self, obj):
        return obj.album_id.album_name if obj.album_id else None


@admin.register(AlbumTrack)
class AlbumTrackAdmin(admin.ModelAdmin):
    list_display = ('track_id', 'album', 'artist', 'track_num', 'track_name', 'is_available')
    search_fields = ('album_id__album_name', 'album_id__album_artist__artist_name', 'track_name', 'feat_artist')
    list_filter = (
        ('album_id__album_name', DropdownFilter),
        ('album_id__album_artist__artist_name', DropdownFilter),
        (AvailableTracksFilter),
    )
    
    def album(self, obj):
        return obj.album_id.album_name if obj.album_id else ''
    
    def artist(self, obj):
        return obj.album_id.album_artist.artist_name if obj.album_id else ''
    
    def is_available(self, obj):
        return 'yes' if obj.song_id else ''
    
    def get_exclude(self, request, obj=None):
        if obj is None:
            return ['track_id']
        return []
    
    def save_model(self, request, obj, form, change):
        if not obj.track_id:
            random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            while AlbumTrack.objects.filter(track_id=random_part).exists():
                random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            obj.track_id = random_part
        super().save_model(request, obj, form, change)
