from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from .models import Profile, Skill, Project, SocialLink

# ============================================================
# API JSON del portfolio
# ============================================================
# Las vistas son funciones de Python que reciben una "request"
# (petición del navegador) y devuelven una "response" (respuesta).
# Aquí devolvemos JSON usando JsonResponse (sin Django REST Framework).
#
# En desarrollo el frontend llama a /api/... y el proxy de Vite
# reenvía esa petición a Django (localhost:8000). Así no hay CORS.
# ============================================================


def _build_image_url(request, image_field):
    """
    Devuelve la URL completa de una imagen (para que el frontend
    pueda cargarla), o None si el proyecto no tiene imagen.

    request.build_absolute_uri() convierte "/media/x.png" en
    "http://localhost:8000/media/x.png".
    """
    if not image_field:
        return None
    return request.build_absolute_uri(image_field.url)


def portfolio_api(request):
    """
    Vista principal: devuelve TODO el contenido del portfolio
    (perfil, habilidades, proyectos y redes sociales) en un solo
    JSON. Así el frontend hace una única petición a /api/.
    """
    # --- Perfil (primer registro de la tabla Profile) ---
    profile = Profile.objects.first()

    # --- Habilidades agrupadas por categoría ---
    # Con values_list sacamos las categorías distintas, sin repetir.
    # order_by('category') para que salgan ordenadas.
    categories = (
        Skill.objects.values_list("category", flat=True)
        .order_by("category")
        .distinct()
    )

    # Para cada categoría, guardamos sus habilidades en una lista.
    skills_by_category = []
    for category in categories:
        skills_by_category.append(
            {
                "category": category,
                "items": list(
                    Skill.objects.filter(category=category).values_list("name", flat=True)
                ),
            }
        )

    # --- Proyectos (ordenados por el campo 'order') ---
    projects = []
    for project in Project.objects.all():
        projects.append(
            {
                "id": project.id,
                "title": project.title,
                "description": project.description,
                # 'technologies' es un texto "a, b, c"; lo partimos en lista.
                "technologies": [
                    tech.strip()
                    for tech in (project.technologies or "").split(",")
                    if tech.strip()
                ],
                "url_github": project.url_github,
                "url_demo": project.url_demo,
                "image": _build_image_url(request, project.image),
                "order": project.order,
            }
        )

    # --- Redes sociales ---
    social_links = list(
        SocialLink.objects.values("label", "url", "icon").order_by("id")
    )

    # Construimos el JSON final con todo el contenido.
    data = {
        "profile": {
            "name": profile.name if profile else None,
            "title": profile.title if profile else None,
            "summary": profile.summary if profile else None,
            "email": profile.email if profile else None,
        },
        "skills": skills_by_category,
        "projects": projects,
        "social_links": social_links,
    }

    # JsonResponse convierte el diccionario a JSON automáticamente.
    # safe=False solo es necesario si devolviéramos una lista.
    return JsonResponse(data)


@require_GET
def health_check(request):
    """
    Pequeño endpoint de prueba para comprobar que la API responde.
    Accesible en /api/health/
    """
    return JsonResponse({"status": "ok"})


def spa(request, *args, **kwargs):
    """
    Vista para PRODUCCIÓN: sirve el build de React (frontend/dist/index.html)
    en cualquier ruta que no sea /api/ ni /admin/. Esto convierte el sitio en
    una SPA (Single Page Application): el navegador carga index.html y React
    se encarga de mostrar la sección correcta.

    En desarrollo NO se usa: la página la sirve Vite en el puerto 5173.
    """
    try:
        return render(request, "index.html")
    except Exception:
        # Si aún no existe el build de React, mostramos un aviso.
        return JsonResponse(
            {
                "detail": (
                    "Frontend no construido todavía. "
                    "Ejecuta: cd frontend && npm install && npm run build"
                )
            },
            status=404,
        )
