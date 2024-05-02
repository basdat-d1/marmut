# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.downloaded_songs, name='downloaded_songs'),
]
