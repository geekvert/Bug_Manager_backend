from django.contrib import admin
from django.urls import path, include
from backend import urls as backend_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('backend/', include(backend_urls)),
    path('djrichtextfield/', include('djrichtextfield.urls')),
]
