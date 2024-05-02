from django.urls import path
from podcast.views import *

app_name = 'podcast'

urlpatterns = [
    path('', daftar_podcast, name='daftar_podcast'),
    path('daftar-episode/', daftar_episode, name='daftar_episode'),
]