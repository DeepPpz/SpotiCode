from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from spoticode.web import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('spoticode.web.urls')),
    path('accounts/', include('spoticode.accounts.urls')),
    path('common/', include('spoticode.common.urls')),
    path('albums/', include('spoticode.albums.urls')),
    path('artists/', include('spoticode.artists.urls')),
    path('playlists/', include('spoticode.playlists.urls')),
    path('songs/', include('spoticode.songs.urls')),
    # path('tasks/', include('spoticode.tasks.urls')),
]

handler404 = 'spoticode.web.views.custom_404_view'
handler500 = 'spoticode.web.views.custom_500_view'

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
