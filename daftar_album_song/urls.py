from django.urls import path
from . import views

app_name = 'daftar_album_song'

# Explicit view imports to ensure they're loaded
from .views import (
    get_albums, get_album_detail, get_songs, get_popular_songs, get_new_releases,
    get_user_albums, get_user_songs, create_album, create_song,
    delete_album, delete_song, get_label_albums, get_label_album_songs,
    delete_label_album, delete_label_song, get_all_labels, get_all_artists,
    get_all_songwriters, get_all_genres
)

urlpatterns = [
    # REST API endpoints
    path('albums/', get_albums, name='get_albums_api'),
    path('albums/<str:album_id>/', get_album_detail, name='album_detail_api'),
    path('songs/', get_songs, name='get_songs_api'),
    path('songs/<str:song_id>/', delete_song, name='delete_song_api_alt'),
    path('songs/popular/', get_popular_songs, name='popular_songs_api'),
    path('songs/new/', get_new_releases, name='new_releases_api'),
    
    # Feature 13: Artist/Songwriter Album & Song Management
    path('user-albums/', get_user_albums, name='get_user_albums_api'),
    path('user-songs/', get_user_songs, name='get_user_songs_api'),
    path('create-album/', create_album, name='create_album_api'),
    path('create-song/', create_song, name='create_song_api'),
    path('album/<str:album_id>/delete/', delete_album, name='delete_album_api'),

    path('song/<str:song_id>/delete/', delete_song, name='delete_song_api'),
    
    # Feature 16: Label Album & Song Management
    path('label-albums/', get_label_albums, name='get_label_albums_api'),
    path('label-album/<str:album_id>/songs/', get_label_album_songs, name='get_label_album_songs_api'),
    path('label-album/<str:album_id>/delete/', delete_label_album, name='delete_label_album_api'),
    path('label-song/<str:song_id>/delete/', delete_label_song, name='delete_label_song_api'),
    path('labels/', get_all_labels, name='get_all_labels_api'),
    path('artists/', get_all_artists, name='get_all_artists_api'),
    path('songwriters/', get_all_songwriters, name='get_all_songwriters_api'),
    path('genres/', get_all_genres, name='get_all_genres_api'),
]