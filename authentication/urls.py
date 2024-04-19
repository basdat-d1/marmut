from django.urls import path
from .views import authentication, register, login

app_name = 'authentication'

urlpatterns = [
    path('', authentication, name='authentication'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
]