from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django_admin_listfilter_dropdown.filters import DropdownFilter
# Project
from spoticode.accounts.admin_filters import GroupsFilter, LoggedFilter


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 
                    'group', 'is_active', 'is_staff', 'is_superuser', 'last_login')
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = (
        ('is_active', DropdownFilter),
        ('is_staff', DropdownFilter),
        ('is_superuser', DropdownFilter),
        (GroupsFilter),
        (LoggedFilter),
    )
    
    def group(self, obj):
        return obj.groups.first().name if obj.groups.exists() else None

    group.short_description = 'group'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
