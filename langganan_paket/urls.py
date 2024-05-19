from django.urls import path
from .views import langganan_paket, pembayaran_paket, riwayat_transaksi
from django.contrib.auth import views as auth_views

app_name = 'langganan_paket'

urlpatterns = [
    path('', langganan_paket, name='langganan_paket'),
    path('pembayaran_paket/', pembayaran_paket, name='pembayaran_paket'),
    path('riwayat_transaksi/', riwayat_transaksi, name='riwayat_transaksi'),
]