from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


class GroupsFilter(admin.SimpleListFilter):
    title = _('Group')
    parameter_name = 'group'

    def lookups(self, request, model_admin):
        groups = Group.objects.all().values_list('name', 'name')
        return tuple(groups) + (('None', _('None')),)

    def queryset(self, request, queryset):
        if self.value() and self.value() != 'None':
            return queryset.filter(groups__name=self.value())
        elif self.value() == 'None':
            return queryset.filter(groups__isnull=True)


class LoggedFilter(admin.SimpleListFilter):
    title = _('Logged')
    parameter_name = 'is_logged'

    def lookups(self, request, model_admin):
        return (
            ('Logged', _('Logged')),
            ('Not Logged', _('Not Logged')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'Logged':
            return queryset.filter(last_login__isnull=False)
        elif self.value() == 'Not Logged':
            return queryset.filter(last_login__isnull=True)
