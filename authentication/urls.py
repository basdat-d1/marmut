from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    # Feature 2: Login and Logout
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('me/', views.current_user, name='current_user'),
    
    # Feature 3: Registration
    path('register/user/', views.register_user, name='register_user'),
    path('register/label/', views.register_label, name='register_label'),
    
    # CSRF Token
    path('csrf-token/', views.get_csrf_token, name='csrf_token'),
]