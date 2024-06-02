from django.contrib import admin
# Project
from spoticode.artists.models import Artist, ArtistLink
from spoticode.artists.admin_filters import ArtistsFirstLetterFilter, ArtistLinksFilter


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('artist_id', 'artist_name', 'other_names', 'songs_count', 'albums_count')
    search_fields = ('artist_name', 'other_names')
    list_filter = (
        (ArtistsFirstLetterFilter),
    )
    
    def get_exclude(self, request, obj=None):
        if obj is None:
            return ['songs_count', 'albums_count']
        return []


@admin.register(ArtistLink)
class ArtistLinkAdmin(admin.ModelAdmin):
    list_display = ('artist', 'official_website', 'spotify_link', 'wikipedia_link', 'rateyourmusic_link')
    search_fields = ('artist_id__artist_name', 'artist_id__other_names')
    list_filter = (
        (ArtistLinksFilter),
        (ArtistsFirstLetterFilter), 
    )
    
    def artist(self, obj):
        return obj.artist_id.artist_name if obj.artist_id else ''
