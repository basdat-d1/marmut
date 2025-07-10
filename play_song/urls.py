from django.urls import path
from . import views

app_name = 'play_song'

urlpatterns = [
    # REST API endpoints
    path('<str:song_id>/', views.get_song_detail, name='get_song_detail_api'),
    path('<str:song_id>/play/', views.play_song, name='play_song_api'),
    path('<str:song_id>/download/', views.download_song, name='download_song_api'),
    path('<str:song_id>/add-to-playlist/', views.add_to_playlist, name='add_to_playlist_api'),
    path('playlists/', views.get_user_playlists_for_song, name='get_playlists_for_song_api'),
    # Tambahan: POST ke <song_id>/ diarahkan ke play_song
    path('<str:song_id>/', views.play_song, name='play_song_post_api'),
]