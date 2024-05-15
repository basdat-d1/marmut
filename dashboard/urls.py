from django.urls import path
from .views import (dashboard_pengguna_biasa, dashboard_premium, dashboard_artist_songwriter, 
                    dashboard_podcaster, dashboard_label, dashboard_pengguna)

urlpatterns = [
    path('pengguna-biasa/', dashboard_pengguna_biasa, name='dashboard_pengguna_biasa'),
    path('premium/', dashboard_premium, name='dashboard_premium'),
    path('artist-songwriter/', dashboard_artist_songwriter, name='dashboard_artist_songwriter'),
    path('podcaster/', dashboard_podcaster, name='dashboard_podcaster'),
    path('label/', dashboard_label, name='dashboard_label'),
    path('pengguna/', dashboard_pengguna, name='dashboard_pengguna'),
]