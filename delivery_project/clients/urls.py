from django.urls import path
from . import views

app_name = 'clients'

urlpatterns = [
    path('', views.client, name='create'),
    path('list/', views.list, name='list'),
    path('<str:pk>/detail/', views.detail, name='detail'),
    path('<str:pk>/edit/', views.client, name='edit'),
    path('<str:pk>/delete/', views.delete_client, name='delete'),
]