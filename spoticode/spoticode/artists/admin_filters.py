from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# Project
from spoticode.artists.models import Artist


class ArtistsFirstLetterFilter(admin.SimpleListFilter):
    title = _('First Letter')
    parameter_name = 'artist_name'
    
    def lookups(self, request, model_admin):
        all_artist_names = Artist.objects.values_list('artist_name', flat=True)
        first_letters = sorted(set(name[0].upper() for name in all_artist_names if name))
        return tuple((letter, letter) for letter in first_letters)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(artist_name__istartswith=self.value())
        return queryset


class ArtistLinksFilter(admin.SimpleListFilter):
    title = _('Links')
    parameter_name = 'links'

    def lookups(self, request, model_admin):
        return (
            ('With Official Website', _('With Official Website')),
            ('No Official Website', _('No Official Website')),
            ('With Spotify', _('With Spotify')),
            ('No Spotify', _('No Spotify')),
            ('With Wikipedia', _('With Wikipedia')),
            ('No Wikipedia', _('No Wikipedia')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'With Official Website':
            return queryset.filter(official_website__isnull=False)
        elif self.value() == 'No Official Website':
            return queryset.filter(official_website__isnull=True)
        elif self.value() == 'With Spotify':
            return queryset.filter(spotify_link__isnull=False)
        elif self.value() == 'No Spotify':
            return queryset.filter(spotify_link__isnull=True)
        elif self.value() == 'With Wikipedia':
            return queryset.filter(wikipedia_link__isnull=False)
        elif self.value() == 'No Wikipedia':
            return queryset.filter(wikipedia_link__isnull=True)
