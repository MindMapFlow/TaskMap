from django.urls import path
from . import views

urlpatterns = [
    path('sign-in/', views.sign_in_view, name='sign_in'),
    path('sign-up/', views.sign_up_view, name='sign_up'),
    path('logout/', views.logout_view, name='logout'),
]
