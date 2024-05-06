from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


def custom_login_required(func):
    decorated_view_func = login_required(func)
    
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return decorated_view_func(request, *args, **kwargs)
        else:
            return redirect('user_login')

    return wrapper


def can_create_or_update(func):
    actual_decorator = user_passes_test(
        lambda u: u.groups.filter(name__in=['Admin', 'Moderator', 'Editor']).exists(),
        login_url ='/unauthorized/'
    )
    
    if func:
        return actual_decorator(func)
    
    return actual_decorator


def can_delete(func):
    actual_decorator = user_passes_test(
        lambda u: u.groups.filter(name__in=['Admin', 'Moderator']).exists(),
        login_url ='/unauthorized/'
    )
    
    if func:
        return actual_decorator(func)
    
    return actual_decorator


def can_read(func):
    actual_decorator = user_passes_test(
        lambda u: u.groups.filter(name__in=['Admin', 'Moderator', 'Editor', 'Viewer']).exists(),
        login_url ='/unauthorized/'
    )
    
    if func:
        return actual_decorator(func)
    
    return actual_decorator


def is_staff(func):
    actual_decorator = user_passes_test(
        lambda u: u.is_staff,
        login_url ='/unauthorized/'
    )
    
    if func:
        return actual_decorator(func)
    
    return actual_decorator
