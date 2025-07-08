from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Feature 4: Dashboard
    path('', views.dashboard, name='dashboard'),
    path('stats/', views.user_stats, name='user_stats'),
]