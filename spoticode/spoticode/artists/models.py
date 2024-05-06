from django.db import models


class Artist(models.Model):
    ID_MAX_LENGTH = 5
    COUNTER_DEFAULT = 0
    
    artist_id = models.CharField(primary_key=True, max_length=ID_MAX_LENGTH, 
                                 db_column='artist_id', verbose_name='Artist ID')
    artist_name = models.CharField(unique=True, 
                                   db_column='artist_name', verbose_name='Artist')
    other_names = models.CharField(null=True, blank=True, 
                                   db_column='other_names', verbose_name='Other Names')
    songs_count = models.IntegerField(blank=True, default=COUNTER_DEFAULT, 
                                      db_column='songs_count', verbose_name='Total Songs')
    albums_count = models.IntegerField(blank=True, default=COUNTER_DEFAULT, 
                                       db_column='albums_count', verbose_name='Total Albums')
    
    def __str__(self):
        return self.artist_name

    class Meta:
        db_table = 'artists'
        ordering = ('artist_name',)
        verbose_name = 'Artist'
        verbose_name_plural = 'Artists'


class ArtistLink(models.Model):
    artist_id = models.OneToOneField(Artist, to_field='artist_id', on_delete=models.CASCADE, 
                                     primary_key=True, 
                                     db_column='artist_id', verbose_name='Artist ID')
    official_website = models.URLField(null=True, blank=True, unique=True, 
                                       db_column='official_website', verbose_name='Official Website')
    spotify_link = models.URLField(null=True, blank=True, unique=True, 
                                   db_column='spotify_link', verbose_name='Spotify Link')
    wikipedia_link = models.URLField(null=True, blank=True, unique=True, 
                                     db_column='wikipedia_link', verbose_name='Wikipedia Link')

    class Meta:
        db_table = 'artists_links'
        ordering = ('artist_id',)
        verbose_name = 'Artist Link'
        verbose_name_plural = 'Artists Links'
