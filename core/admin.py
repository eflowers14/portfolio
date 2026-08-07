from django.contrib import admin

from .models import Profile, Skill, Project, SocialLink

# ============================================================
# Panel de administración de Django
# ============================================================
# Registrar un modelo aquí hace que aparezca en /admin/ y puedas
# crear/editar/borrar registros desde el navegador.
# ============================================================


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista de perfiles
    list_display = ("name", "title", "email")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    # Filtros laterales por categoría
    list_filter = ("category",)
    # Ordena por categoría y luego por nombre
    ordering = ("category", "name")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "url_demo")
    # Habilita la reordenación arrastrando en la lista
    list_editable = ("order",)
    ordering = ("order",)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("label", "url", "icon")
