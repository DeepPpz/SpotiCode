from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class AlbumsReleaseDateFilter(admin.SimpleListFilter):
    title = _('Release Date')
    parameter_name = 'release_date'

    def lookups(self, request, model_admin):
        return (
            ('1900-1989', _('1900-1989')),
            ('1990-1999', _('1990-1999')),
            ('2000-2010', _('2000-2010')),
            ('2011-2020', _('2011-2020')),
            ('2021-2030', _('2021-2030')),
            ('None', _('None')),
        )

    def queryset(self, request, queryset):
        if self.value() == '1900-1989':
            return queryset.filter(release_date__range=['1900-01-01', '1989-12-31'])
        elif self.value() == '1990-1999':
            return queryset.filter(release_date__range=['1990-01-01', '1999-12-31'])
        elif self.value() == '2000-2010':
            return queryset.filter(release_date__range=['2000-01-01', '2010-12-31'])
        elif self.value() == '2011-2020':
            return queryset.filter(release_date__range=['2011-01-01', '2020-12-31'])
        elif self.value() == '2021-2030':
            return queryset.filter(release_date__range=['2021-01-01', '2030-12-31'])
        elif self.value() == 'None':
            return queryset.filter(release_date__isnull=True)


class AlbumLinksFilter(admin.SimpleListFilter):
    title = _('Links')
    parameter_name = 'links'

    def lookups(self, request, model_admin):
        return (
            ('With Spotify', _('With Spotify')),
            ('No Spotify', _('No Spotify')),
            ('With Wikipedia', _('With Wikipedia')),
            ('No Wikipedia', _('No Wikipedia')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'With Spotify':
            return queryset.filter(spotify_link__isnull=False)
        elif self.value() == 'No Spotify':
            return queryset.filter(spotify_link__isnull=True)
        elif self.value() == 'With Wikipedia':
            return queryset.filter(wikipedia_link__isnull=False)
        elif self.value() == 'No Wikipedia':
            return queryset.filter(wikipedia_link__isnull=True)
