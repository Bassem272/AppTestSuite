# accounts/urls.py
from django.urls import path
from .views import app_list, app_create, app_update, app_delete

urlpatterns = [
    path('', app_list, name='app_list'),
    path('new/', app_create, name='app_create'),
    path('<int:pk>/edit/', app_update, name='app_update'),
    path('<int:pk>/delete/', app_delete, name='app_delete'),
]
