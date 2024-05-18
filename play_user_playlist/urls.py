from django.urls import path
from .views import play_user_playlist

app_name = 'play_user_playlist'

urlpatterns = [
     path('<str:id_user_playlist>', play_user_playlist, name='play_user_playlist')
]