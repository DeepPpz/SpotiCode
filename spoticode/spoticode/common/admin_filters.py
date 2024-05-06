from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# Project
from spoticode.common.models import Genre


class GenresFirstLetterFilter(admin.SimpleListFilter):
    title = _('First Letter')
    parameter_name = 'genre_name'
    
    def lookups(self, request, model_admin):
        all_genres_names = Genre.objects.values_list('genre_name', flat=True)
        first_letters = sorted(set(name[0].upper() for name in all_genres_names if name))
        return tuple((letter, letter) for letter in first_letters)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(genre_name__istartswith=self.value())
        return queryset
