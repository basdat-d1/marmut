from django.urls import path
from . import views

app_name = 'podcast'

urlpatterns = [
    # REST API endpoints
    path('', views.get_user_podcasts, name='get_user_podcasts_api'),
    path('create/', views.create_podcast, name='create_podcast_api'),
    path('<str:podcast_id>/delete/', views.delete_podcast, name='delete_podcast_api'),
    path('<str:podcast_id>/episodes/', views.get_podcast_episodes, name='get_podcast_episodes_api'),
    path('<str:podcast_id>/episodes/create/', views.create_episode, name='create_episode_api'),
    path('<str:podcast_id>/episodes/<str:episode_id>/delete/', views.delete_episode, name='delete_episode_api'),
    path('genres/', views.get_available_genres, name='get_available_genres_api'),
]