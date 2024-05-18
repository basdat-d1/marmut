from django.urls import path
from .views import (user_playlist, tambah_playlist, ubah_playlist, hapus_playlist, detail_playlist, 
                    tambah_lagu_playlist, hapus_lagu_playlist)

app_name = 'user_playlist'

urlpatterns = [
    path('', user_playlist, name='user_playlist'),
    path('tambah_playlist/', tambah_playlist, name='tambah_playlist'),
    path('ubah_playlist/<str:id_user_playlist>/', ubah_playlist, name='ubah_playlist'),
    path('hapus_playlist/<str:id_user_playlist>/', hapus_playlist, name='hapus_playlist'),
    path('detail_playlist/<str:id_user_playlist>/', detail_playlist, name='detail_playlist'),
    path('tambah_lagu/<str:id_user_playlist>/', tambah_lagu_playlist, name='tambah_lagu_playlist'),
    path('hapus_lagu/<str:id_user_playlist>/<str:id_song>/', hapus_lagu_playlist, name='hapus_lagu_playlist'),
]