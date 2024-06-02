import random, string
# Django
from django.db import models


class Playlist(models.Model):
    COUNTER_DEFAULT = 0
    
    playlist_id = models.CharField(primary_key=True, blank=True, 
                                   db_column='playlist_id', verbose_name='Playlist ID')
    playlist_name = models.CharField(unique=True, 
                                     db_column='playlist_name', verbose_name='Playlist Name')
    songs_local = models.PositiveIntegerField(blank=True, default=COUNTER_DEFAULT, 
                                              db_column='songs_local', verbose_name='Total Songs Local')
    songs_spotify = models.PositiveIntegerField(blank=True, default=COUNTER_DEFAULT, 
                                                db_column='songs_spotify', verbose_name='Total Songs on Spotify')
    playlist_link = models.URLField(null=True, blank=True, unique=True, 
                                    db_column='playlist_link', verbose_name='Playlist Link')
    playlist_image = models.ImageField(null=True, blank=True, 
                                       db_column='playlist_image', verbose_name='Image')
    notes = models.TextField(null=True, blank=True, 
                             db_column='notes', verbose_name='Notes')
    
    def __str__(self):
        return self.playlist_name
    
    def save(self, *args, **kwargs):
        if not self.playlist_id:
            random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            while Playlist.objects.filter(playlist_id=f'PL-{random_part}').exists():
                random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            self.playlist_id = 'PL-' + random_part
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'playlists'
        ordering = ('playlist_name',)
        verbose_name = 'Playlist'
        verbose_name_plural = 'Playlists'


class SongPlaylistRelation(models.Model):
    relation_id = models.CharField(primary_key=True, blank=True, 
                                   db_column='id', verbose_name='ID')
    playlist_id = models.ForeignKey(to='playlists.Playlist', to_field='playlist_id', on_delete=models.CASCADE, 
                                    db_column='playlist_id', verbose_name='Playlist ID')
    song_id = models.ForeignKey(to='songs.Song', to_field='song_id', on_delete=models.CASCADE, 
                                db_column='song_id', verbose_name='Song ID')

    def save(self, *args, **kwargs):
        if not self.relation_id:
            random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
            while SongPlaylistRelation.objects.filter(relation_id=random_part).exists():
                random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
            self.relation_id = random_part  
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'song_playlist_relations'
        unique_together = (('playlist_id', 'song_id'),)
        verbose_name = 'Song-Playlist Relation'
        verbose_name_plural = 'Song-Playlist Relations'
