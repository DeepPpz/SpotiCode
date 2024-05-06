from django.db import models
# Project
from spoticode.artists.models import Artist


class Album(models.Model):
    ALBUM_TYPES = {
        'Anniversary Edition': 'Anniversary Edition',
        'Box Set': 'Box Set',
        'Compilation': 'Compilation',
        'Deluxe Album': 'Deluxe Album',
        'Demo': 'Demo',
        'EP': 'EP',
        'Japanese Edition': 'Japanese Edition',
        'Live Album': 'Live Album',
        'LP': 'LP',
        'Other Special': 'Other Special',
        'Re-Issue Edition': 'Re-Issue Edition',
        'Soundtrack Album': 'Soundtrack Album',
        'Unknown': 'Unknown',
    }
    
    album_id = models.CharField(primary_key=True, blank=True, 
                                db_column='album_id', verbose_name='Album ID')
    release_date = models.DateField(null=True, blank=True, 
                                    db_column='release_date', verbose_name='Release Date')
    album_artist = models.ForeignKey(Artist, to_field='artist_name', on_delete=models.RESTRICT, 
                                     db_column='album_artist', verbose_name='Artist')
    album_name = models.CharField(db_column='album_name', verbose_name='Album')
    album_type = models.CharField(choices=ALBUM_TYPES, default='Unknown', blank=True, 
                                  db_column='album_type', verbose_name='Album Type')
    
    def __str__(self):
        return f'{self.album_name} by {self.album_artist.artist_name}'
    
    def save(self, *args, **kwargs):
        if not self.album_id:
            artist_id = self.album_artist.artist_id
            album_no = self.album_artist.albums_count + 1
            self.album_id = f'{artist_id}-A{album_no:02}'
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'albums'
        ordering = ('album_artist', 'album_name')
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'


class AlbumLink(models.Model):
    album_id = models.OneToOneField(Album, to_field='album_id', on_delete=models.CASCADE, 
                                    primary_key=True, 
                                    db_column='album_id', verbose_name='Album ID')
    spotify_link = models.URLField(null=True, blank=True, 
                                   db_column='spotify_link', verbose_name='Spotify URL')
    wikipedia_link = models.URLField(null=True, blank=True, 
                                     db_column='wikipedia_link', verbose_name='Wikipedia URL')
    
    class Meta:
        db_table = 'albums_links'
        ordering = ('album_id',)
        verbose_name = 'Album Link'
        verbose_name_plural = 'Albums Links'
