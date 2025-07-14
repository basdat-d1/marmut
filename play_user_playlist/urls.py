from django.urls import path
from . import views

app_name = 'play_user_playlist'

urlpatterns = [
    path('<str:id_user_playlist>/', views.play_user_playlist, name='play_user_playlist_api'),
    path('<str:id_user_playlist>/song/<str:song_id>/', views.play_song_from_playlist, name='play_song_from_playlist_api'),
]