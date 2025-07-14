from django.urls import path
from . import views

app_name = 'search_bar'

urlpatterns = [
    path('', views.search, name='search'),
    path('songs/', views.search_songs, name='search_songs'),
    path('podcasts/', views.search_podcasts, name='search_podcasts'),
    path('playlists/', views.search_playlists, name='search_playlists'),
    path('item/<str:item_id>/', views.get_item_detail, name='item_detail'),
]