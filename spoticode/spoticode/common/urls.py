from django.urls import path, include
# Project
from spoticode.common import views


urlpatterns = [
    path('music_groups/', include([
        path('all/', views.show_all_music_groups, name='music_groups_all'),
        path('create/', views.create_music_group, name='music_group_create'),
        
        path('<str:id>/', include([
            path('details/', views.show_details_music_group, name='music_group_details'),
            path('delete/', views.delete_music_group, name='music_group_delete'),
            path('edit/', views.edit_music_group, name='music_group_edit'),
        ])),
   ])),
    
    path('genres/', include([
        path('all/', views.show_all_genres, name='genres_all'),
        path('create/', views.create_genre, name='genre_create'),
        
        path('<str:id>/', include([
            path('details/', views.show_details_genre, name='genre_details'),
            path('delete/', views.delete_genre, name='genre_delete'),
            path('edit/', views.edit_genre, name='genre_edit'),
        ])),
    ]))
]
