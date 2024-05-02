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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    # path('album-song/', include('album_song.urls')),
    # path('cek-royalti/', include('cek_royalti.urls')),
    # path('daftar-album-song/', include('daftar_album_song.urls')),
    path('dashboard/', include('dashboard.urls')),
    # path('downloaded-songs/', include('downloaded_songs.urls')),
    # path('langganan-paket/', include('langganan_paket.urls')),
    # path('lihat-chart/', include('lihat_chart.urls')),
    # path('play-podcast/', include('play_podcast.urls')),
    path('play-song/', include('play_song.urls')),
    path('play-user-playlist/', include('play_user_playlist.urls')),
    # path('search-bar/', include('search_bar.urls')),
    path('user-playlist/', include('user_playlist.urls')),
]