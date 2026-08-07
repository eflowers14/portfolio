"""
Comando de gestión: python manage.py seed

Rellena la base de datos con el contenido del portfolio.
Puede ejecutarse todas las veces que quieras: usa update_or_create,
así que NO crea registros duplicados (si el registro ya existe,
solo lo actualiza).
"""
import shutil
from pathlib import Path

from django.core.management.base import BaseCommand

from core.models import Profile, Skill, Project, SocialLink

# ------------------------------------------------------------
# CONTENIDO
# ------------------------------------------------------------
# Definimos todos los datos en estas listas/diccionarios para que
# sea fácil editarlos y re-ejecutar el seed.
# ------------------------------------------------------------

PROFILE_DATA = {
    "name": "Enrique Alejandro Flores Marín",
    "title": "Ingeniero Informático",
    "summary": (
        "Ingeniero informático entusiasmado con el software, el hardware, "
        "el desarrollo y el manejo de datos. Apasionado por la transparencia "
        "y la protección de los datos. Amante de opencode y con ganas de "
        "contribuir a la sociedad."
    ),
    "email": "enriquealejandrofloresmarin@gmail.com",
}

# Cada categoría es un diccionario: {"categoría": ["habilidad1", ...]}
SKILLS_DATA = [
    {"category": "Lenguajes", "items": ["Python", "JavaScript", "TypeScript", "C", "Java"]},
    {"category": "Frameworks", "items": ["Django", "React"]},
    {"category": "Bases de datos", "items": ["PostgreSQL", "SQLite"]},
    {"category": "Herramientas", "items": ["Docker", "Vite", "Tailwind", "Supabase", "Git"]},
]

# Rutas de las imágenes ORIGINALES en tu disco (las copiaremos a media/projects/)
PROJECT_IMAGES = {
    "Comida Clara": Path(r"D:\Code\ComidaClara.png"),
    "Mayte Canvas": Path(r"D:\Code\MayteCanvas.png"),
    "Remesas Express": Path(r"D:\Code\RemesasExpress.png"),
}

# order -> menor número, aparece primero
PROJECTS_DATA = [
    {
        "title": "Comida Clara",
        "description": (
            "Web que permite indicar los ingredientes que tienes en casa y te da "
            "una lista de los platos posibles, ordenados por la menor cantidad "
            "de ingredientes a usar."
        ),
        "technologies": "TypeScript, JavaScript, CSS, TanStack, Vite, Vercel",
        "url_github": "https://github.com/eflowers14/comidaclara",
        "url_demo": "https://comidaclara.vercel.app/",
        "order": 1,
    },
    {
        "title": "Mayte Canvas",
        "description": (
            "Web collage de las pinturas hechas por mi tía. Fue mi primera web "
            "pagada, por eso le tengo cariño, además recibo dinero por cada "
            "pintura vendida."
        ),
        "technologies": "TypeScript, JavaScript, CSS, Tailwind, Vercel",
        "url_github": "https://github.com/eflowers14/mayteCanvas",
        "url_demo": "https://mayte-canvas.vercel.app/",
        "order": 2,
    },
    {
        "title": "Remesas Express",
        "description": (
            "Web para mostrar los precios actuales de mis remesas. Los clientes "
            "entran directamente, ven cuánto dinero ganarían y las cuentas a "
            "las que depositar."
        ),
        "technologies": "TypeScript, JavaScript, CSS, TanStack, Vite, PostgreSQL, Supabase, Vercel",
        "url_github": "https://github.com/eflowers14/remesas-express",
        "url_demo": "https://remesasexpress.vercel.app/",
        "order": 3,
    },
]

SOCIAL_LINKS_DATA = [
    {"label": "GitHub", "url": "https://github.com/eflowers14", "icon": "github"},
    {
        # NOTA: no pude verificar este enlace (LinkedIn bloquea búsquedas).
        # Revisa tu perfil y actualiza la URL aquí si no es la correcta.
        "label": "LinkedIn",
        "url": "https://www.linkedin.com/in/enrique-alejandro-flores-marin/",
        "icon": "linkedin",
    },
    {"label": "Twitter/X", "url": "https://x.com/eflowersssss", "icon": "twitter"},
    {"label": "YouTube", "url": "https://www.youtube.com/@eflowersssss", "icon": "youtube"},
]


class Command(BaseCommand):
    help = "Rellena la base de datos con el contenido del portfolio (re-ejecutable)."

    def handle(self, *args, **options):
        # self.stdout es la forma correcta de imprimir mensajes en un comando
        self.stdout.write("Cargando datos...")

        # Limpiamos los datos previos para que el seed sea determinista:
        # así no quedan registros viejos ni duplicados al volver a ejecutarlo.
        Profile.objects.all().delete()
        Skill.objects.all().delete()
        Project.objects.all().delete()
        SocialLink.objects.all().delete()

        # 1) Perfil: get_or_create por email (clave única)
        profile, created = Profile.objects.get_or_create(
            email=PROFILE_DATA["email"], defaults=PROFILE_DATA
        )
        # Si ya existía, lo actualizamos con los datos nuevos
        for field, value in PROFILE_DATA.items():
            setattr(profile, field, value)
        profile.save()
        self.stdout.write(self.style.SUCCESS(f"  Perfil listo: {profile.name}"))

        # 2) Habilidades: update_or_create por (nombre, categoría)
        for skill_data in SKILLS_DATA:
            for skill_name in skill_data["items"]:
                skill, created = Skill.objects.update_or_create(
                    name=skill_name,
                    category=skill_data["category"],
                )
        self.stdout.write(self.style.SUCCESS("  Habilidades listas"))

        # 3) Proyectos + copiar imágenes
        #    update_or_create por 'title' para no duplicar.
        for project_data in PROJECTS_DATA:
            project, created = Project.objects.update_or_create(
                title=project_data["title"],
                defaults={
                    "description": project_data["description"],
                    "technologies": project_data["technologies"],
                    "url_github": project_data["url_github"],
                    "url_demo": project_data["url_demo"],
                    "order": project_data["order"],
                },
            )

            # Copiamos la imagen a media/projects/<slug>.png
            source = PROJECT_IMAGES[project_data["title"]]
            if source.exists():
                dest_dir = Path("media") / "projects"
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest = dest_dir / f"{project.title.lower().replace(' ', '-')}.png"
                shutil.copyfile(source, dest)
                # Guardamos la ruta en el campo ImageField
                project.image = f"projects/{dest.name}"
                project.save()

        self.stdout.write(self.style.SUCCESS("  Proyectos listos"))

        # 4) Redes sociales: update_or_create por url
        for social_data in SOCIAL_LINKS_DATA:
            link, created = SocialLink.objects.update_or_create(
                url=social_data["url"],
                defaults={"label": social_data["label"], "icon": social_data["icon"]},
            )
        self.stdout.write(self.style.SUCCESS("  Enlaces sociales listos"))

        self.stdout.write(
            self.style.SUCCESS("Seed completado. ¡Todo el contenido está cargado!")
        )
