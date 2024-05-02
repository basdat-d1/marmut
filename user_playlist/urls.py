from django.urls import path
from .views import (user_playlist, tambah_playlist, ubah_playlist, detail_playlist, tambah_lagu)

app_name = 'user_playlist'

urlpatterns = [
    path('', user_playlist, name='user_playlist'),
    path('tambah/', tambah_playlist, name='tambah_playlist'),
    path('ubah/', ubah_playlist, name='ubah_playlist'),
    path('detail/', detail_playlist, name='detail_playlist'),
    path('tambah-lagu/', tambah_lagu, name='tambah_lagu'),
]