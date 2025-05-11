from django.urls import path
from . import views
from .views import theory_view

urlpatterns = [
    path('', views.index, name='index_old'),
    path('archive-material/', views.archive_material, name='archive_material'),
    path('achievements/', views.theory_view, name='theory_view'),  # должно вести на theory_view
path('material/', views.theory_view, name='main_material'),  # если хочешь использовать имя main_material

]


