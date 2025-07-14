from django.urls import path
from . import views

app_name = 'cek_royalti'

urlpatterns = [
    path('', views.get_royalty_info, name='get_royalty_info_api'),
    path('label/', views.get_label_royalty_info, name='get_label_royalty_info_api'),
    path('update/', views.update_royalty_info, name='update_royalty_info_api'),
]