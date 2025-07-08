from django.urls import path
from . import views

app_name = 'downloaded_songs'

urlpatterns = [
    # REST API endpoints
    path('', views.get_downloaded_songs, name='get_downloaded_songs_api'),
    path('<str:song_id>/remove/', views.remove_downloaded_song, name='remove_downloaded_song_api'),
    path('stats/', views.get_download_stats, name='download_stats_api'),
]