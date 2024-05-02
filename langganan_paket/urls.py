from django.urls import path
from . import views

urlpatterns = [
    path('', views.langganan_paket, name='langganan_paket'),
    path('pembayaran_paket/', views.pembayaran_paket, name='pembayaran_paket'),
    path('riwayat_transaksi/', views.riwayat_transaksi, name='riwayat_transaksi'),
]
