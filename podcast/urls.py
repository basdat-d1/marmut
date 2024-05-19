from django.urls import path
from podcast.views import *

app_name = 'podcast'

urlpatterns = [
    path('', daftar_podcast, name='daftar_podcast'),
    path('daftar-episode/', daftar_episode, name='daftar_episode'),
    path('add-podcast/', add_podcast, name='add_podcast'),    
    path('remove-podcast/', remove_podcast, name='remove_podcast'), 
    path('add-episode/', add_episode, name='add_episode'),     
    path('remove-episode/', remove_episode, name='remove_episode'),       
]