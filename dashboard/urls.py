from django.urls import path
from .views import dashboard_pengguna_biasa, dashboard_artist_songwriter, dashboard_podcaster, dashboard_label

urlpatterns = [
    path('pengguna-biasa/', dashboard_pengguna_biasa, name='dashboard_pengguna_biasa'),
    path('artist-songwriter/', dashboard_artist_songwriter, name='dashboard_artist_songwriter'),
    path('podcaster/', dashboard_podcaster, name='dashboard_podcaster'),
    path('label/', dashboard_label, name='dashboard_label'),
]