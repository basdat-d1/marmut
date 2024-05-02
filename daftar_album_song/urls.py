from django.urls import path
from .views import (list_album, create_album, update_album, list_song, create_song, update_song)

app_name = 'daftar_album_song'

urlpatterns = [
    path('list-album/1', list_album, name='list-album/1'),
    path('create-album/1', create_album, name='create-album/1'),
    path('edit-album/1', update_album, name='edit-album/1'),
    path('list-album/1/songs', list_song, name='list-album/1/songs'),
    path('create-song/1', create_song, name='create-song/1'),
    path('edit-song/1', update_song, name='edit-song/1'),
]