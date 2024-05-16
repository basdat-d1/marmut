from django.urls import path

from dashboard.views import dashboard_pengguna
from .views import (authentication, register, login,
                    register_pengguna, register_label)

app_name = 'authentication'

urlpatterns = [
    path('', authentication, name='authentication'),
    path('register/', register, name='register'),
    path('register/pengguna/', register_pengguna, name='register_pengguna'),
    path('register/label/', register_label, name='register_label'),
    path('login/', login, name='login'),
    path('pengguna/', dashboard_pengguna, name='dashboard_pengguna'),
]