# Django
from django.urls import path
# Project
from spoticode.web import views

urlpatterns = [
    path('', views.show_homepage, name='homepage'),
    path('about/', views.show_about_page, name='about_page'),
    path('unauthorized/', views.show_unauthorized_page, name='unauthorized_access'),
]
