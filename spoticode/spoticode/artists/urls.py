from django.urls import path, include
# Project
from spoticode.artists import views


urlpatterns = [
    path('all/', views.show_all_artists, name='artists_all'),
    path('create/', views.create_artist, name='artist_create'),
    
    path('<str:id>/', include([
        path('details/', views.show_details_artist, name='artist_details'),
        path('delete/', views.delete_artist, name='artist_delete'),
        
        path('edit/', include([
            path('info/', views.edit_artist_info, name='artist_info_edit'),
            path('links/', views.edit_artist_links, name='artist_links_edit'),
        ])),
    ])),
]
