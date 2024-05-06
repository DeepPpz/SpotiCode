from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class SongsAlbumsNoAlbumsFilter(admin.SimpleListFilter):
    title = _('Album Relations')
    parameter_name = 'album_relations'

    def lookups(self, request, model_admin):
        return (
            ('Singles', _('Singles')),
            ('Album-Related', _('Album-Related')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Singles':
            return queryset.filter(album_id__isnull=True)
        elif self.value() == 'Album-Related':
            return queryset.filter(album_id__isnull=False)


class SongsLinksNoLinksFilter(admin.SimpleListFilter):
    title = _('Spotify Links')
    parameter_name = 'spotify_link'

    def lookups(self, request, model_admin):
        return (
            ('No Links', _('No Links')),
            ('With Links', _('With Links')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'No Links':
            return queryset.filter(spotify_link__isnull=True)
        elif self.value() == 'With Links':
            return queryset.filter(spotify_link__isnull=False)
