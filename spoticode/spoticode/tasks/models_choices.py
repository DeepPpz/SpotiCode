from django.apps import apps
from django.contrib.auth.models import User


def get_app_choices():
    """
    Dynamically generate choices for app names.
    """
    app_configs = apps.get_app_configs()
    return [(app_config.label, app_config.verbose_name) for app_config in app_configs]


def get_default_user():
    try:
        return User.objects.get(username='deleted.users')
    except User.DoesNotExist:
        raise User.DoesNotExist('User "deleted.users" does not exist.')
