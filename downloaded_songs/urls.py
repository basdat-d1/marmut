# urls.py
from django.urls import path
from .views import downloaded_songs, get_downloaded_songs

app_name = 'downloaded_songs'

urlpatterns = [
    path('', downloaded_songs, name='downloaded_songs'),
    path('api/get_downloaded_songs/', get_downloaded_songs, name='get_downloaded_songs'),
]
