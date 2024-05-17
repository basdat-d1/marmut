# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.downloaded_songs, name='downloaded_songs'),
    path('api/get_downloaded_songs/', views.get_downloaded_songs, name='get_downloaded_songs'),
]
