import random, string
# Django
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Song(models.Model):
    YEAR_MIN_VALUE = 1860
    YEAR_MAX_VALUE = 2500
    
    song_id = models.CharField(primary_key=True, blank=True, 
                               db_column='song_id', verbose_name='Song ID')
    song_title = models.CharField(db_column='song_title', verbose_name='Title')
    main_artist = models.ForeignKey(to='artists.Artist', to_field='artist_name', on_delete=models.RESTRICT, 
                                    db_column='main_artist', verbose_name='Artist')
    feat_artist = models.CharField(null=True, blank=True, 
                                   db_column='feat_artist', verbose_name='Feat. Artists')
    genre = models.ForeignKey(to='common.Genre', to_field='genre_name', on_delete=models.RESTRICT, 
                              null=True, blank=True, 
                              db_column='genre', verbose_name='Genre')
    song_year = models.IntegerField(null=True, blank=True, 
                                    validators=[MinValueValidator(YEAR_MIN_VALUE, 'First recording is in 1860. Have you found new history?'), 
                                                MaxValueValidator(YEAR_MAX_VALUE, 'Woah, are you coming from the future?')], 
                                    db_column='song_year', verbose_name='Release Year')
    group = models.ForeignKey(to='common.MusicGroup', to_field='group_name', on_delete=models.SET_DEFAULT, 
                              blank=True, default='Unspecified', 
                              db_column='group', verbose_name='Group')
    album_id = models.ForeignKey(to='albums.Album', to_field='album_id', on_delete=models.RESTRICT, 
                                 null=True, blank=True, 
                                 db_column='album_id', verbose_name='Album')
    spotify_link = models.URLField(unique=True, null=True, blank=True, 
                                   db_column='spotify_link', verbose_name='Spotify Link')

    def __str__(self):
        if self.feat_artist is not None:
            return f'"{self.song_title}" by {self.main_artist.artist_name} (feat. {self.feat_artist})'
        else:
            return f'"{self.song_title}" by {self.main_artist.artist_name}'
    
    def save(self, *args, **kwargs):
        if not self.song_id:
            artist_id = self.main_artist.artist_id
            song_no = self.main_artist.songs_count + 1
            self.song_id = f'{artist_id}{song_no:03}'
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'songs'
        unique_together = (('song_title', 'main_artist'),)
        ordering = ('main_artist', 'song_title')
        verbose_name = 'Song'
        verbose_name_plural = 'Songs'


class PendingSong(models.Model):
    pending_id = models.CharField(primary_key=True, blank=True, 
                                  db_column='pending_id', verbose_name='ID')
    song_title = models.CharField(db_column='song_title', verbose_name='Title')
    main_artist = models.CharField(db_column='main_artist', verbose_name='Artist')
    feat_artist = models.CharField(null=True, blank=True, 
                                   db_column='feat_artist', verbose_name='Feat. Artist')
    to_group = models.ForeignKey(to='common.MusicGroup', to_field='group_name', on_delete=models.SET_DEFAULT, 
                                 blank=True, default='Unspecified', 
                                 db_column='to_group', verbose_name='Group')
    is_added = models.BooleanField(blank=True, default=False, 
                                   db_column='is_added', verbose_name='Added')
    new_artist = models.BooleanField(blank=True, default=False, 
                                     db_column='new_artist', verbose_name='New Artist')
    
    def __str__(self):
        if self.feat_artist is not None:
            return f'"{self.song_title}" by {self.main_artist} (feat. {self.feat_artist})'
        else:
            return f'"{self.song_title}" by {self.main_artist}'

    def save(self, *args, **kwargs):
        if not self.pending_id:            
            random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
            while PendingSong.objects.filter(pending_id=random_part).exists():
                random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
            self.pending_id = random_part
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'pending_songs'
        unique_together = (('song_title', 'main_artist'),)
        ordering = ('main_artist', 'song_title')
        verbose_name = 'Pending Song'
        verbose_name_plural = 'Pending Songs'
