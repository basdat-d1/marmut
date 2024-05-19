from django.urls import path
from .views import downloaded_songs, get_downloaded_songs, delete_downloaded_song

app_name = 'downloaded_songs'

urlpatterns = [
    path('', downloaded_songs, name='downloaded_songs'),
    path('api/get_downloaded_songs/', get_downloaded_songs, name='get_downloaded_songs'),
    path('delete/<str:song_id>/', delete_downloaded_song, name='delete_downloaded_song'),
]