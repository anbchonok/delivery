from django.urls import path
from . import views

app_name = 'containers'

urlpatterns = [
    path('', views.ContainersCreateView.as_view(), name='create'),
    path('list/', views.ContainersListView.as_view(), name='list'),
    path('<int:pk>/', views.ContainersDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.ContainersUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.ContainersDeleteView.as_view(), name='delete'),
]
