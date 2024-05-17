from django.urls import path
from .views import play_song, tambah_lagu_play_song, download_song

app_name = 'play_song'

urlpatterns = [
    path('<str:id_konten>/', play_song, name="play_song"),
    path('tambah_lagu_play_song/<uuid:id_konten>/', tambah_lagu_play_song, name='tambah_lagu_play_song'),
    path('download_song/<uuid:id_konten>/', download_song, name="download_song"),
]