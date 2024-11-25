from django.urls import path, include
# Project
from spoticode.playlists import views


urlpatterns = [
    path('all/', views.show_all_playlists, name='playlists_all'),
    path('create/', views.create_playlist, name='playlist_create'),
    
    path('<str:id>/', include([
        path('details/', views.show_details_playlist, name='playlist_details'),
        path('delete/', views.delete_playlist, name='playlist_delete'),
        path('edit/', views.edit_playlist_info, name='playlist_edit'),
        
        # Song-Playlist Relations
        path('songs_list/', views.show_all_playlist_songs, name='playlist_songs_all'),
        path('preview_mass_add/', views.select_songs_for_mass_add, name='playlist_songs_preview_mass_add'),
        path('mass_add/', views.mass_add_songs, name='playlist_songs_mass_add'),
        path('delete_song/<str:s_id>/', views.delete_song_from_playlist, name='playlist_song_delete'),
    ])),
]