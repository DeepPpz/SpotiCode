from django.urls import path, include
# Project
from spoticode.albums import views


urlpatterns = [
    path('all/', views.show_all_albums, name='albums_all'),
    path('create/', views.create_album, name='album_create'),
    
    path('<str:id>/', include([
        path('details/', views.show_details_album, name='album_details'),
        path('delete/', views.delete_album, name='album_delete'),
        
        path('edit/', include([
            path('info/', views.edit_album_info, name='album_info_edit'),
            path('links/', views.edit_album_links, name='album_links_edit'),
        ])),
        
        path('track/', include([
            path('create/', views.create_album_track, name='album_track_create'),
            path('<str:tr_id>/', include([
                path('delete/', views.delete_album_track, name='album_track_delete'),
                path('edit/', views.edit_album_track, name='album_track_edit'),
            ])),
        ])),
    ])),
]
