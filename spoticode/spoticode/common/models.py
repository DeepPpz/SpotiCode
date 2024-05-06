import random, string
# Django
from django.db import models


class MusicGroup(models.Model):
    GROUP_NAME_MAX_LENGTH = 100
    COUNTER_DEFAULT = 0
    
    id = models.CharField(primary_key=True, blank=True, 
                          db_column='id', verbose_name='ID')
    group_name = models.CharField(max_length=GROUP_NAME_MAX_LENGTH, unique=True, 
                                  db_column='group_name', verbose_name='Group Name')
    songs_count = models.IntegerField(blank=True, default=COUNTER_DEFAULT, 
                                      db_column='songs_count', verbose_name='Total Songs')
    pending_count = models.IntegerField(blank=True, default=COUNTER_DEFAULT, 
                                        db_column='pending_count', verbose_name='Pending Songs')
    
    def __str__(self):
        return self.group_name
    
    def save(self, *args, **kwargs):
        if not self.id:
            random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
            while MusicGroup.objects.filter(id=random_part).exists():
                random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
            self.id = random_part
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'music_groups'
        ordering = ('group_name',)
        verbose_name = 'Music Group'
        verbose_name_plural = 'Music Groups'


class Genre(models.Model):
    GENRE_NAME_MAX_LENGTH = 100
    COUNTER_DEFAULT = 0
    
    id = models.CharField(primary_key=True, blank=True, 
                          db_column='id', verbose_name='ID')
    genre_name = models.CharField(max_length=GENRE_NAME_MAX_LENGTH, unique=True, 
                                  db_column='genre_name', verbose_name='Genre')
    songs_count = models.IntegerField(default=COUNTER_DEFAULT, 
                                      db_column='songs_count', verbose_name='Total Songs')
    
    def __str__(self):
        return self.genre_name
    
    def save(self, *args, **kwargs):
        if not self.id:
            random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
            while Genre.objects.filter(id=random_part).exists():
                random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
            self.id = random_part
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'genres'
        ordering = ('genre_name',)
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
