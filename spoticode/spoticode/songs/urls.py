from django.urls import path, include
# Project
from spoticode.songs import views


urlpatterns = [
    path('', include([
        path('all/', views.show_all_songs, name='songs_all'),
        path('create/', views.create_song, name='song_create'),
        
        path('<str:id>/', include([
            path('details/', views.show_details_song, name='song_details'),
            path('delete/', views.delete_song, name='song_delete'),
            path('edit/', views.edit_song, name='song_edit'),
            path('add_to_playlist/', views.add_song_to_playlist, name='song_add_to_playlist'),
        ])),
   ])),
    
    path('pending_songs/', include([
        path('all/', views.show_all_pending_songs, name='pending_songs_all'),
        path('create/', views.create_pending_song, name='pending_song_create'),
        path('delete/added/', views.delete_added_pending_songs, name='pending_song_multiple_delete'),
        
        path('<str:id>/', include([
            path('details/', views.show_details_pending_song, name='pending_song_details'),
            path('delete/', views.delete_pending_song, name='pending_song_delete'),
            path('edit/', views.edit_pending_song, name='pending_song_edit'),
        ])),
    ]))
]
