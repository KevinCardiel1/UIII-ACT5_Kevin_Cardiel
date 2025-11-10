# backend_DisneyStore/urls.py

from django.contrib import admin
from django.urls import path, include # Importa include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_Disney.urls')), # <--- Enlaza las URLs de app_Disney aquí
]

# Para servir archivos de medios (imágenes) en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)