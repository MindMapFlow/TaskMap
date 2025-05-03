from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_app.urls')),
    path('', include('core.urls')),
    path('tests/', include('archive_test.urls')),

]
