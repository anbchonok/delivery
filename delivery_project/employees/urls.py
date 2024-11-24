from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
    path('', views.EmployeesCreateView.as_view(), name='create'),
    path('list/', views.EmployeesListView.as_view(), name='list'),
    path('<int:pk>/', views.EmployeesDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.EmployeesUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.EmployeesDeleteView.as_view(), name='delete')
]
