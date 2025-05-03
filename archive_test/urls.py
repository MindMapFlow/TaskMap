from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_list, name='archive_tests'),
    path('<str:language>/', views.test_detail, name='test_detail'),
]
