from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.langganan_paket, name='langganan_paket'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('pembayaran_paket/', views.pembayaran_paket, name='pembayaran_paket'),
    path('riwayat_transaksi/', views.riwayat_transaksi, name='riwayat_transaksi'),
]
