from django.urls import path
from .views import (list_album, create_album, list_song, create_song, list_album_label, list_song_label, delete_song,
                    delete_album, delete_album_label)
from daftar_album_song.views import list_song, list_album

app_name = 'daftar_album_song'

urlpatterns = [
    path('list-album/', list_album, name='list_album'),
    path('create-album/', create_album, name='create_album'),
    path('list-album/list-song/', list_song, name='list_song'),
    path('list-album/create-song/', create_song, name='create_song'),
    path('list-album/label/', list_album_label, name='list_album_label'),
    path('list-album/list-song/label/', list_song_label, name='list_song_label'),
    path('list-album/list-song/delete-song/', delete_song, name='delete_song'),
    path('list-album/delete-album/', delete_album, name='delete_album'),
    path('list-album/delete-album/label/', delete_album_label, name='delete_album_label'),
]