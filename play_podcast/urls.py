from django.urls import path
from . import views

app_name = 'play_podcast'

urlpatterns = [
    path('', views.get_all_podcasts, name='get_all_podcasts_api'),
    path('<str:podcast_id>/', views.get_podcast_detail, name='get_podcast_detail_api'),
    path('<str:podcast_id>/episodes/<str:episode_id>/play/', views.play_podcast_episode, name='play_podcast_episode_api'),
]