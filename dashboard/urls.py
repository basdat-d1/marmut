from django.urls import path
from .views import dashboard_pengguna, dashboard_label

app_name = 'dashboard'

urlpatterns = [
    path('pengguna/', dashboard_pengguna, name='dashboard_pengguna'),
    path('label/', dashboard_label, name='dashboard_label'),
    path('pengguna/', dashboard_pengguna, name='dashboard_pengguna'),
]