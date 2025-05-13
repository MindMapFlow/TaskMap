from django.urls import path
from . import views

urlpatterns = [
    path('', views.language_list, name='language_list'),
    path('<int:language_id>/', views.tests_by_language, name='tests_by_language'),
path('start/<int:test_id>/', views.test_start, name='test_start'),
]
