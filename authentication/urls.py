from django.urls import path
from .views import register, login

app_name = 'authentication'

urlpatterns = [
  path('register/', register, name='register'),
  path('login/', login, name='login'),
]