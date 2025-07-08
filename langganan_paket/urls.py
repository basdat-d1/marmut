from django.urls import path
from . import views

app_name = 'langganan_paket'

urlpatterns = [
    # REST API endpoints
    path('packages/', views.get_packages, name='get_packages_api'),
    path('', views.get_user_subscription, name='get_subscription_api'),
    path('subscribe/', views.subscribe_package, name='subscribe_api'),
    path('cancel/', views.cancel_subscription, name='cancel_subscription_api'),
    path('history/', views.get_subscription_history, name='subscription_history_api'),
    path('transaction-history/', views.transaction_history, name='transaction_history_api'),
    path('current/', views.current_subscription, name='current_subscription_api'),
    path('payment-methods/', views.payment_methods, name='payment_methods_api'),
]