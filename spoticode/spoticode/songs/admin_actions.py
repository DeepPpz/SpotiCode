from django.contrib import admin
# Project
from spoticode.artists.models import Artist
from spoticode.common.models import MusicGroup
from spoticode.songs.models import Song


@admin.action(description='Mark songs as Added')
def make_added(modeladmin, request, queryset):
    queryset.update(is_added=True)


@admin.action(description='Save songs in database')
def copy_to_songs_table(modeladmin, request, queryset):
    for new_song in queryset:
        artist = Artist.objects.get(artist_name=new_song.main_artist)
        group = MusicGroup.objects.get(group_name=new_song.to_group)
        
        Song.objects.create(
            song_title=new_song.song_title,
            main_artist=artist,
            feat_artist=new_song.feat_artist,
            the_group=group,
    )
