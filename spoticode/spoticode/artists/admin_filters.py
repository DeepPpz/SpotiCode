from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# Project
from spoticode.artists.models import Artist


class ArtistsFirstLetterFilter(admin.SimpleListFilter):
    title = _('First Letter')
    parameter_name = 'artist_name_letter'
    
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
            ('official_website', _('Official Website')),
            ('no_official_website', _('No Official Website')),
            ('spotify', _('Spotify')),
            ('no_spotify', _('No Spotify')),
            ('wikipedia', _('Wikipedia')),
            ('no_wikipedia', _('No Wikipedia')),
            ('rateyourmusic', _('RateYourMusic')),
            ('no_rateyourmusic', _('No RateYourMusic')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'official_website':
            return queryset.filter(official_website__isnull=False)
        elif self.value() == 'no_official_website':
            return queryset.filter(official_website__isnull=True)
        elif self.value() == 'spotify':
            return queryset.filter(spotify_link__isnull=False)
        elif self.value() == 'no_spotify':
            return queryset.filter(spotify_link__isnull=True)
        elif self.value() == 'wikipedia':
            return queryset.filter(wikipedia_link__isnull=False)
        elif self.value() == 'no_wikipedia':
            return queryset.filter(wikipedia_link__isnull=True)
        elif self.value() == 'rateyourmusic':
            return queryset.filter(rateroumusic_link__is_null=False)
        elif self.value() == 'no_rateyourmusic':
            return queryset.filter(rateroumusic_link__is_null=True)
