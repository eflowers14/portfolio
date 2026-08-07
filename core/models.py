from django.db import models

# ============================================================
# Modelos de la base de datos
# ============================================================
# Un modelo es una "tabla" en la base de datos. Cada clase que
# definas aquí se convierte en una tabla, y cada campo (atributo)
# en una columna de esa tabla.
#
# Después de tocar este archivo hay que crear una migración:
#     python manage.py makemigrations core
# y aplicarla:
#     python manage.py migrate
# ============================================================


class Profile(models.Model):
    """
    Perfil personal (nombre, título, resumen y email).
    Solo debe existir UN registro, por eso se llama "registro único".
    """

    # CharField -> texto corto (nombre, título, email)
    name = models.CharField(max_length=100, verbose_name="Nombre")
    title = models.CharField(max_length=100, verbose_name="Título")
    summary = models.TextField(verbose_name="Resumen")  # TextField -> texto largo
    email = models.EmailField(unique=True, verbose_name="Email")  # unique=True -> no se repite

    def __str__(self):
        # Lo que se muestra en el panel admin y en la consola
        return self.name

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"


class Skill(models.Model):
    """
    Habilidad con una categoría (ej: "Lenguajes", "Frameworks").
    """

    name = models.CharField(max_length=100, verbose_name="Nombre")
    category = models.CharField(max_length=100, verbose_name="Categoría")

    def __str__(self):
        # Ejemplo: "Python (Lenguajes)"
        return f"{self.name} ({self.category})"

    class Meta:
        verbose_name = "Habilidad"
        verbose_name_plural = "Habilidades"


class Project(models.Model):
    """
    Proyecto del portfolio: título, descripción, tecnologías,
    enlaces a GitHub/demo, imagen y un orden de aparición.
    """

    title = models.CharField(max_length=100, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")

    # Los campos de abajo pueden estar vacíos (blank=True en el admin,
    # null=True en la base de datos) porque no todos los proyectos
    # tienen GitHub o demo, por ejemplo.
    technologies = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        verbose_name="Tecnologías (separadas por coma)",
    )
    url_github = models.URLField(
        blank=True, null=True, verbose_name="URL de GitHub"
    )
    url_demo = models.URLField(blank=True, null=True, verbose_name="URL de demo")
    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        null=True,
        verbose_name="Imagen",
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden (menor = primero)",
        help_text="Los proyectos se ordenan de menor a mayor",
    )

    class Meta:
        ordering = ["order"]  # Por defecto, ordena por el campo 'order'
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"

    def __str__(self):
        return self.title


class SocialLink(models.Model):
    """
    Red social o enlace de contacto: etiqueta, url e icono.
    """

    label = models.CharField(max_length=100, verbose_name="Etiqueta (ej: GitHub)")
    url = models.URLField(verbose_name="URL")
    icon = models.CharField(
        max_length=100,
        verbose_name="Icono",
        help_text="Nombre del icono (ej: github, linkedin, twitter, youtube)",
    )

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Enlace social"
        verbose_name_plural = "Enlaces sociales"
