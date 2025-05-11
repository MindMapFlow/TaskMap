from django.urls import path
from . import views
from .views import theory_view

urlpatterns = [
    path('archive-material/', views.archive_material, name='archive_material'),
    path('material/', views.theory_view, name='theory_view'),  # ✅ оставить только этот
]
