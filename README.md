# Portfolio Personal — Enrique Alejandro Flores Marín

Portfolio de una sola página hecho con **Django** (backend + API JSON) y
**React + Vite** (frontend). En español, con diseño blanco/negro y acentos
plateados y azules.

---

## Índice

1. [Qué hay dentro de este proyecto](#qué-hay-dentro-de-este-proyecto)
2. [Cómo funciona (arquitectura)](#cómo-funciona-arquitectura)
3. [Primeros pasos en Windows](#primeros-pasos-en-windows)
4. [Poner en marcha en desarrollo](#poner-en-marcha-en-desarrollo)
5. [Crear un superusuario (panel admin)](#crear-un-superusuario-panel-admin)
6. [El comando seed (datos de ejemplo)](#el-comando-seed-datos-de-ejemplo)
7. [Producción (servir React desde Django)](#producción-servir-react-desde-django)
8. [Estructura de carpetas](#estructura-de-carpetas)
9. [Cómo editar el contenido](#cómo-editar-el-contenido)
10. [Errores comunes](#errores-comunes)

---

## Qué hay dentro de este proyecto

| Parte     | Tecnología      | Para qué sirve                                        |
| --------- | --------------- | ----------------------------------------------------- |
| Backend   | Django + SQLite | Guarda los datos (perfil, habilidades, proyectos...)  |
| API       | Django (JSON)   | Entrega los datos al frontend por `GET /api/`         |
| Frontend  | React + Vite    | La página web que ve el visitante                     |
| Admin     | Django Admin    | Panel web para editar todo el contenido (`/admin/`)   |
| Seed      | Comando Django  | Rellena la base de datos con tu contenido (`seed`)    |

---

## Cómo funciona (arquitectura)

```
Navegador
   │
   ├── En DESARROLLO:
   │       http://localhost:5173   ← Vite sirve React
   │              │
   │              └── fetch('/api/')  → PROXY de Vite → Django :8000
   │
   └── En PRODUCCIÓN:
           http://localhost:8000   ← Django sirve la página + la API
                  │
                  ├── /api/    → respuesta JSON
                  └── /        → el build de React (frontend/dist)
```

- **En desarrollo** abres `http://localhost:5173`. Vite tiene un **proxy**
  configurado en `frontend/vite.config.js` que reenvía cualquier petición a
  `/api` hacia Django (`localhost:8000`). Por eso no necesitas CORS.
- **En producción** Django sirve tanto la API (`/api/`) como el build de
  React (`frontend/dist`) desde la raíz.

---

## Primeros pasos en Windows

Necesitas tener instalados:

- **Python 3.10 o superior** (comprueba con `python --version`)
- **Node.js 18 o superior** (comprueba con `node --version`)

### 1. Crear el entorno virtual

Un entorno virtual aísla las librerías de Python de este proyecto del resto
de tu sistema. Se crea **una sola vez**.

```powershell
python -m venv venv
```

Actívalo (hay que hacerlo **cada vez** que abras una terminal nueva):

```powershell
.\venv\Scripts\Activate.ps1
```

> Si PowerShell te da un error de permisos, ejecuta primero:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

Después de activarlo, la terminal muestra `(venv)` al inicio.

### 2. Instalar las dependencias de Python

```powershell
pip install -r requirements.txt
```

Esto instala Django y Pillow (necesaria para manejar imágenes).

### 3. Instalar las dependencias del frontend

```powershell
cd frontend
npm install
cd ..
```

---

## Poner en marcha en desarrollo

### Terminal 1 — Django (puerto 8000)

```powershell
.\venv\Scripts\python.exe manage.py runserver
```

Si es la **primera vez**, antes ejecuta las migraciones y carga los datos:

```powershell
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py seed
```

### Terminal 2 — Vite (puerto 5173)

```powershell
cd frontend
npm run dev
```

Ahora abre **http://localhost:5173** en tu navegador. ¡Ya está tu portfolio!

> Comprueba que la API responde en http://localhost:8000/api/

---

## Crear un superusuario (panel admin)

El superusuario es la cuenta de administrador para entrar en
**http://localhost:8000/admin/**. Se crea **una sola vez** (más adelante
puedes crear más usuarios desde el propio admin).

```powershell
.\venv\Scripts\python.exe manage.py createsuperuser
```

Te pedirá un **nombre de usuario**, un **email** y una **contraseña**.
Después entra en `http://localhost:8000/admin/` con esas credenciales y
podrás editar todo el contenido desde el navegador.

---

## El comando seed (datos de ejemplo)

`seed` rellena la base de datos con todo tu contenido (perfil, habilidades,
proyectos, redes sociales) sin necesidad de escribirlo a mano en el admin.

```powershell
.\venv\Scripts\python.exe manage.py seed
```

Es **re-ejecutable**: puedes lanzarlo las veces que quieras y no creará
registros duplicados (usa `update_or_create`).

> El código está en `core/management/commands/seed.py`. Si cambias algo ahí
> (por ejemplo, la URL de LinkedIn), vuelve a ejecutar `seed`.

### Las imágenes de los proyectos

El seed copia las imágenes desde las rutas que se indican al principio de
`seed.py` (por defecto `D:\Code\ComidaClara.png`, etc.) a la carpeta
`media/projects/`. Si tu carpeta es otra, edita `PROJECT_IMAGES` en ese
archivo.

---

## Producción (servir React desde Django)

Para cuando quieras desplegar la página (no para desarrollo):

```powershell
cd frontend
npm run build          # genera frontend/dist con la versión final
cd ..
.\venv\Scripts\python.exe manage.py collectstatic
```

Con esto, al arrancar Django (`runserver` o un servidor real), la raíz
`http://localhost:8000/` ya mostrará la página completa servida por Django.

> Recuerda: en producción cambia `DEBUG = False` y `ALLOWED_HOSTS` en
> `portfolio/settings.py` antes de subirla a internet.

---

## Estructura de carpetas

```
portfolio/
├── manage.py                  # Utilidad principal de Django (migrate, runserver...)
├── requirements.txt           # Dependencias de Python
├── portfolio/
│   ├── settings.py            # Configuración del proyecto
│   ├── urls.py                # Rutas del proyecto (/api/, /admin/...)
│   └── ...
├── core/
│   ├── models.py              # Las tablas: Profile, Skill, Project, SocialLink
│   ├── views.py               # La API JSON (/api/) y la vista SPA
│   ├── admin.py               # Registro de los modelos en el panel admin
│   └── management/commands/seed.py   # Comando para cargar datos
├── media/projects/            # Imágenes de los proyectos (las copia el seed)
└── frontend/
    ├── vite.config.js         # Configuración de Vite (proxy de /api)
    ├── index.html             # Plantilla HTML de la SPA
    └── src/
        ├── App.jsx            # Componente principal (pide los datos a /api/)
        ├── index.css          # Todos los estilos
        └── components/        # Navbar, Hero, About, Projects, Contact, Footer
```

---

## Cómo editar el contenido

| Qué quieres cambiar            | Dónde                                          |
| ------------------------------ | ---------------------------------------------- |
| Tu nombre, título o email      | `seed.py` (o en el admin)                      |
| Habilidades                    | `seed.py` o admin → Habilidades                |
| Proyectos / imágenes / enlaces | `seed.py` o admin → Proyectos                  |
| Redes sociales                 | `seed.py` o admin → Enlaces sociales           |
| Colores y diseño               | `frontend/src/index.css` (variables `:root`)   |
| Textos de las secciones        | `frontend/src/components/*.jsx`                |

Después de cambiar el **backend** (models.py, seed.py...), ejecuta:

```powershell
.\venv\Scripts\python.exe manage.py makemigrations core
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py seed
```

Después de cambiar el **frontend**, Vite recarga solo (hot reload). No hace
falta reiniciar nada.

---

## Errores comunes

- **`No module named django`** → el entorno virtual no está activado, o no
  ejecutaste `pip install -r requirements.txt`.
- **`No puedo conectar con la API`** en el frontend → Django no está
  corriendo (o no está en el puerto 8000). Revisa la Terminal 1.
- **La página sale en blanco** → prueba `npm run dev` en la carpeta
  `frontend` y asegúrate de que Vite dice "ready in".
- **Las imágenes no aparecen** → ejecuta `manage.py seed` (las copia) y
  comprueba que las rutas de `PROJECT_IMAGES` en `seed.py` existen.
- **El admin en español sale raro** → normal, es la traducción automática
  de Django. `LANGUAGE_CODE = 'es'` está en `settings.py`.

---

¡Disfruta construyendo y personalizando tu portfolio! 🚀
