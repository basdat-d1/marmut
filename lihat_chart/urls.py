from django.urls import path
from lihat_chart.views import *

app_name = 'lihat_chart'

urlpatterns = [
    path('', show_chart, name='show_chart'),
    path('lihat-playlist/', show_playlist, name='show_playlist'),
]