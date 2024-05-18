from django.urls import path
from .views import (list_album, create_album, update_album, list_song, create_song, update_song, list_album_label, list_song_label)

app_name = 'daftar_album_song'

urlpatterns = [
    path('list-album/', list_album, name='list-album/'),
    path('create-album/1', create_album, name='create-album/1'),
    path('edit-album/1', update_album, name='edit-album/1'),
    path('list-album/1/songs', list_song, name='list-album/1/songs'),
    path('list-album/1/create-song/1', create_song, name='list-album/1/create-song/1'),
    path('list-album/1/edit-song/1', update_song, name='list-album/1/edit-song/1'),
    path('list-album/label/1', list_album_label, name='list-album/label/1'),
    path('list-album/label/1/songs', list_song_label, name='list-album/label/1/songs'),
]