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
    
    # 1. Authentication & Registration (Features 2-3)
    path('api/auth/', include('authentication.urls')),
    
    # 2. Dashboard (Feature 4)
    path('api/dashboard/', include('dashboard.urls')),
    
    # 3. User Playlist Management (Feature 5)
    path('api/user-playlist/', include('user_playlist.urls')),
    
    # 4. Subscription Management (Feature 6)
    path('api/subscription/', include('langganan_paket.urls')),
    
    # 5. Search (Feature 7)
    path('api/search/', include('search_bar.urls')),
    
    # 6. Play Song (Feature 8)
    path('api/play-song/', include('play_song.urls')),
    
    # 7. Downloaded Songs (Feature 9)
    path('api/downloads/', include('downloaded_songs.urls')),
    
    # 8. Play Podcast (Feature 10)
    path('api/play-podcast/', include('play_podcast.urls')),
    
    # 9. Play User Playlist (Feature 11)
    path('api/play-user-playlist/', include('play_user_playlist.urls')),
    
    # 10. Charts (Feature 12)
    path('api/chart/', include('lihat_chart.urls')),
    
    # 11. Album & Song Management (Features 13 & 16)
    path('api/album-song/', include('daftar_album_song.urls')),
    
    # 12. Royalty Check (Feature 14)
    path('api/royalty/', include('cek_royalti.urls')),
    
    # 13. Podcast Management (Feature 15)
    path('api/podcast/', include('podcast.urls')),
]