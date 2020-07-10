from django.contrib import admin
from django.urls import path, include
from backend import urls as backend_urls
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('backend/', include(backend_urls)),
    path('djrichtextfield/', include('djrichtextfield.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
