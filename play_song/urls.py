from django.urls import path
from .views import play_song, add_song_to_user_playlist, download_song

app_name = 'play_song'

urlpatterns = [
    path('<str:id_konten>/', play_song, name="play_song"),
    path('add_song_to_user_playlist/<str:id_konten>/', add_song_to_user_playlist, name='add_song_to_user_playlist'),
    path('download_song/<str:id_konten>/', download_song, name="download_song"),
]