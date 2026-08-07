"""
Configuración de URLs del proyecto.

Aquí se define qué hace Django cuando recibe una petición:
   /admin/  -> panel de administración
   /api/    -> nuestra API JSON (la consume React)
   todo lo demás -> la SPA de React (solo en producción)
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path

from core import views

urlpatterns = [
    # Panel de administración: http://localhost:8000/admin/
    path("admin/", admin.site.urls),
    # API JSON del portfolio: http://localhost:8000/api/
    path("api/", views.portfolio_api, name="api"),
    # Comprobación de salud de la API
    path("api/health/", views.health_check, name="health"),
    # Cualquier otra ruta sirve la SPA de React (solo tiene sentido
    # cuando existe el build en frontend/dist). Se pone al final para
    # que no "pise" a las rutas anteriores.
    path("", views.spa, name="spa"),
]

# En desarrollo, Django sirve las imágenes subidas (MEDIA_ROOT).
# Esto es necesario para que se vean las imágenes de los proyectos
# tanto en el admin como en la API.
# (Los archivos static/ los sirve Django automáticamente con runserver)
if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
