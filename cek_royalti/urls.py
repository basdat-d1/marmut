from django.urls import path
from .views import (cek_royalti, cek_royalti_label)

app_name = 'cek_royalti'

urlpatterns = [
    path('', cek_royalti, name='cek_royalti'),
    path('label/', cek_royalti_label, name='cek_royalti_label'),
]