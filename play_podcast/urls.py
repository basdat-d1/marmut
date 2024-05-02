from django.urls import path
from play_podcast.views import *

app_name = 'play_podcast'

urlpatterns = [
    path('', show_podcast, name='show_podcast'),
]