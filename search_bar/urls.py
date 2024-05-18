from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_view, name='search_view'),
    path('detail/<uuid:item_id>/', views.detail_item_view, name='detail_item'),
]