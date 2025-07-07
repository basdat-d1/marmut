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
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.middleware.csrf import get_token

@csrf_exempt
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({'csrf_token': token})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
    path('', include('authentication.urls')),
    path('cek-royalti/', include('cek_royalti.urls')),
    path('daftar-album-song/', include('daftar_album_song.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('downloaded-songs/', include('downloaded_songs.urls')),
    path('langganan-paket/', include('langganan_paket.urls')),
    path('lihat-chart/', include('lihat_chart.urls')),
    path('play-podcast/', include('play_podcast.urls')),
    path('play-song/', include('play_song.urls')),
    path('play-user-playlist/', include('play_user_playlist.urls')),
    path('podcast/', include('podcast.urls')),
    path('search-bar/', include('search_bar.urls')),
    path('user-playlist/', include('user_playlist.urls')),
]