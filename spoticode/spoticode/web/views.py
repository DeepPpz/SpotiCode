import sys
from datetime import datetime
# Django
from django.shortcuts import render


def show_homepage(request):
    context = {
        'curr_year': datetime.now().year,
    }

    return render(request, 'web/homepage.html', context)


def show_about_page(request):
    context = {
        'curr_year': datetime.now().year,
    }

    return render(request, 'web/about.html', context)


def show_unauthorized_page(request):
    context = {
        'curr_year': datetime.now().year,
    }

    return render(request, 'web/unauthorized-access.html', context)


def custom_404_view(request, exception):
    context = {
        'curr_year': datetime.now().year,
    }
    
    return render(request, '404.html', context, status=404)


def custom_500_view(request):
    context = {
        'curr_year': datetime.now().year,
        '500_error': str(sys.exc_info()[1]),
    }
    
    return render(request, '500.html', context, status=500)
