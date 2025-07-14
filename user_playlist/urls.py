from django.urls import path
from . import views

app_name = 'user_playlist'

urlpatterns = [
    path('', views.get_user_playlists, name='get_user_playlists_api'),
    path('create/', views.create_playlist, name='create_playlist_api'),
    path('<str:playlist_id>/', views.get_playlist_detail, name='get_playlist_detail_api'),
    path('<str:playlist_id>/update/', views.update_playlist, name='update_playlist_api'),
    path('<str:playlist_id>/delete/', views.delete_playlist, name='delete_playlist_api'),
    path('<str:playlist_id>/add-song/', views.add_song_to_playlist, name='add_song_to_playlist_api'),
    path('<str:playlist_id>/remove-song/<str:song_id>/', views.remove_song_from_playlist, name='remove_song_from_playlist_api'),
]