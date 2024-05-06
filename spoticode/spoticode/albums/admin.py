from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter
# Project
from spoticode.albums.models import Album, AlbumLink
from spoticode.albums.admin_filters import AlbumsReleaseDateFilter, AlbumLinksFilter


@admin.register(Album)
class AlbumsAdmin(admin.ModelAdmin):
    list_display = ('album_id', 'release_date', 'artist', 'album_name', 'album_type')
    search_fields = ('album_artist__artist_name', 'album_name')
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
        if not obj.album_id:
            artist_id = obj.album_artist.artist_id
            album_no = obj.album_artist.albums_count + 1
            obj.album_id = f'{artist_id}-A{album_no:02}'
        super().save_model(request, obj, form, change)


@admin.register(AlbumLink)
class AlbumLinkAdmin(admin.ModelAdmin):
    list_display = ('album', 'spotify_link', 'wikipedia_link')
    search_fields = ('album_id__album_name', 'album_id__album_artist__artist_name')
    list_filter = (
        (AlbumLinksFilter),
    )
    
    def album(self, obj):
        return obj.album_id.album_name if obj.album_id else None
