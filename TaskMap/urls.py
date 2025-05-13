from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_app.urls')),
    path('', include('core.urls')),
    path('material/', include('material.urls')),
    path('material_test/', include('material_test.urls')),
]
