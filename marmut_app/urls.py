"""
URL configuration for marmut_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from authentication.views import get_csrf_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
    
    path('api/auth/', include('authentication.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/user-playlist/', include('user_playlist.urls')),
    path('api/subscription/', include('langganan_paket.urls')),
    path('api/search/', include('search_bar.urls')),
    path('api/play-song/', include('play_song.urls')),
    path('api/downloads/', include('downloaded_songs.urls')),
    path('api/play-podcast/', include('play_podcast.urls')),
    path('api/play-user-playlist/', include('play_user_playlist.urls')),
    path('api/chart/', include('lihat_chart.urls')),
    path('api/album-song/', include('daftar_album_song.urls')),
    path('api/royalty/', include('cek_royalti.urls')),
    path('api/podcast/', include('podcast.urls')),
]