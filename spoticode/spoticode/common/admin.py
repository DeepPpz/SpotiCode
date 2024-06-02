import random, string
# Django
from django.contrib import admin
# Project
from spoticode.common.models import MusicGroup, Genre
from spoticode.common.admin_filters import GenresFirstLetterFilter


@admin.register(MusicGroup)
class MusicGroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'songs_count', 'pending_count')
    search_fields = ('group_name',)
    
    def get_exclude(self, request, obj=None):
        if obj is None:
            return ['group_id', 'songs_count', 'pending_count']
        return []
    
    def save_model(self, request, obj, form, change):
        if not obj.group_id:
            random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
            while MusicGroup.objects.filter(group_id=random_part).exists():
                random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
            obj.group_id = random_part
        super().save_model(request, obj, form, change)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('genre_name', 'description', 'songs_count')
    search_fields = ('genre_name', 'description')
    list_filter = (
        (GenresFirstLetterFilter),
    )
    
    def get_exclude(self, request, obj=None):
        if obj is None:
            return ['genre_id', 'songs_count']
        return []

    def save_model(self, request, obj, form, change):
        if not obj.genre_id:
            random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
            while Genre.objects.filter(genre_id=random_part).exists():
                random_part = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
            obj.genre_id = random_part
        super().save_model(request, obj, form, change)
