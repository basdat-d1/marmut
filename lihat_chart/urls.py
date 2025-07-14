from django.urls import path
from . import views

app_name = 'lihat_chart'

urlpatterns = [
    path('', views.get_charts, name='get_charts_api'),
    path('<str:chart_type>/', views.get_chart_detail, name='chart_detail_api'),
    path('trending/songs/', views.get_trending_songs, name='trending_songs_api'),
    path('top/downloads/', views.get_top_downloads, name='top_downloads_api'),
]