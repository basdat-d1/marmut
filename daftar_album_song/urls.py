from django.urls import path
from . import views

app_name = 'daftar_album_song'

urlpatterns = [
    # REST API endpoints
    path('albums/', views.get_albums, name='get_albums_api'),
    path('albums/<str:album_id>/', views.get_album_detail, name='album_detail_api'),
    path('songs/', views.get_songs, name='get_songs_api'),
    path('songs/popular/', views.get_popular_songs, name='popular_songs_api'),
    path('songs/new/', views.get_new_releases, name='new_releases_api'),
    
    # Feature 13: Artist/Songwriter Album & Song Management
    path('user-albums/', views.get_user_albums, name='get_user_albums_api'),
    path('create-album/', views.create_album, name='create_album_api'),
    path('create-song/', views.create_song, name='create_song_api'),
    path('album/<str:album_id>/delete/', views.delete_album, name='delete_album_api'),
    path('song/<str:song_id>/delete/', views.delete_song, name='delete_song_api'),
    
    # Feature 16: Label Album & Song Management
    path('label-albums/', views.get_label_albums, name='get_label_albums_api'),
    path('label-album/<str:album_id>/songs/', views.get_label_album_songs, name='get_label_album_songs_api'),
    path('label-album/<str:album_id>/delete/', views.delete_label_album, name='delete_label_album_api'),
    path('label-song/<str:song_id>/delete/', views.delete_label_song, name='delete_label_song_api'),
]