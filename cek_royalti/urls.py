from django.urls import path
from .views import (cek_royalti)

app_name = 'cek-royalti'

urlpatterns = [
    path('cek/1', cek_royalti, name='cek/1'),
]