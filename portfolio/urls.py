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

# Django sirve las imágenes de los proyectos (MEDIA_ROOT) tanto en
# desarrollo como en producción (Render): así /media/... funciona aunque
# DEBUG esté en False. Las imágenes están commiteadas en el repo.
# OJO: static() (django.conf.urls.static) NO añade la ruta cuando
# DEBUG=False, por eso aquí definimos la ruta a mano con serve().
from django.urls import re_path
from django.views.static import serve

urlpatterns += [
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        kwargs={"document_root": settings.MEDIA_ROOT},
    ),
]
