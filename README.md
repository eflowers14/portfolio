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
7. [Despliegue en producción (Vercel + Render)](#despliegue-en-producción-vercel--render)
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
| Despliegue| Vercel + Render | Vercel sirve el frontend; Render sirve la API JSON    |

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
           https://portfolio.vercel.app   ← Vercel sirve el build de React
                  │
                  └── fetch('https://portfolio-7gmi.onrender.com/api/')
                            → Django en Render (API JSON + fotos en /media/)
```

- **En desarrollo** abres `http://localhost:5173`. Vite tiene un **proxy**
  configurado en `frontend/vite.config.js` que reenvía cualquier petición a
  `/api` hacia Django (`localhost:8000`). Por eso no necesitas CORS.
- **En producción** el frontend lo sirve **Vercel** y el backend lo sirve
  **Render** (solo la API en `/api/` y las fotos en `/media/`). Se comunican
  por CORS, ya configurado en `portfolio/settings.py`.

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

Las imágenes viven en `media/projects/` y están **commiteadas en el repo**
(no se ignoran), para que existan también en Render (cuyo disco es
efímero). El seed solo enlaza la ruta en la base de datos. Para cambiar
una imagen, reemplaza el archivo en `media/projects/` y haz commit.

---

## Despliegue en producción (Vercel + Render)

El sitio se despliega en **dos servicios separados** (la rama desplegada es
`elitebook`):

| Servicio | Qué corre                      | URL                                   |
| -------- | ------------------------------ | ------------------------------------- |
| Vercel   | El frontend (build de React)   | `https://portfolio.vercel.app`        |
| Render   | El backend (API JSON de Django)| `https://portfolio-7gmi.onrender.com` |

### Frontend → Vercel

- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Environment**: `VITE_API_URL=https://portfolio-7gmi.onrender.com`
  (sin esta variable, el fetch a `/api/` sería relativo y no funcionaría).

### Backend → Render

- **Root Directory**: la raíz del repo (donde está `manage.py`).
- **Start Command**: `bash render_start.sh`
  (aplica migraciones, carga el `seed` y arranca gunicorn; se usa así porque
  el disco de Render es efímero).
- **Environment**:
  - `SECRET_KEY`: un valor aleatorio (genera uno, p. ej. en https://djecrety.ir).
  - `DEBUG` y `ALLOWED_HOSTS` se configuran solos: `settings.py` detecta
    Render (`RENDER=true`) y apaga DEBUG y añade `.onrender.com` y
    `.vercel.app` automáticamente.

### CORS

`portfolio/settings.py` permite cualquier origen `*.vercel.app` (producción
y previews) mediante `CORS_ALLOWED_ORIGIN_REGEXES`, y el `VITE_API_URL` de
Vercel apunta al dominio de Render. No hace falta tocarlo salvo que quieras
restringir más los orígenes.

### Las fotos y la base de datos

- Las **fotos** de los proyectos están **commiteadas en `media/projects/`**,
  así que existen también en Render (cuyo disco es efímero). Para cambiar
  una, reemplaza el archivo y haz commit.
- La **base de datos es SQLite y efímera**: en cada boot, `render_start.sh`
  ejecuta `migrate` + `seed`, que **borra y recrea todo el contenido**. Por
  eso los cambios que hagas desde el **admin se pierden al reiniciar** el
  servicio. Para editar contenido, modifica `seed.py` y sube los cambios
  (ver [Cómo editar el contenido](#cómo-editar-el-contenido)).
- Si algún día quieres persistencia real (datos y admin que sobrevivan a los
  reinicios), migra a **PostgreSQL** en Render.

---

## Estructura de carpetas

```
portfolio/
├── manage.py                  # Utilidad principal de Django (migrate, runserver...)
├── render_start.sh            # Script de arranque para Render (migrate + seed + gunicorn)
├── requirements.txt           # Dependencias de Python
├── portfolio/
│   ├── settings.py            # Configuración (DEBUG/ALLOWED_HOSTS/CORS automáticos)
│   ├── urls.py                # Rutas (/api/, /admin/...) + servir /media/ en producción
│   └── ...
├── core/
│   ├── models.py              # Las tablas: Profile, Skill, Project, SocialLink
│   ├── views.py               # La API JSON (/api/) y la vista SPA
│   ├── admin.py               # Registro de los modelos en el panel admin
│   └── management/commands/seed.py   # Comando para cargar datos
├── media/projects/            # Imágenes de los proyectos (commiteadas en el repo)
└── frontend/
    ├── vite.config.js         # Configuración de Vite (proxy de /api, base según VERCEL)
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
- **`No puedo conectar con la API`** en desarrollo → Django no está
  corriendo (o no está en el puerto 8000). Revisa la Terminal 1. En
  **producción**, revisa que `VITE_API_URL` está definido en Vercel y que
  el CORS en `settings.py` permite el origen.
- **`Access blocked by CORS` en el navegador** → el origen de Vercel no está
  permitido. Revisa `CORS_ALLOWED_ORIGIN_REGEXES` en `settings.py` y que
  Render tenga desplegado el último commit.
- **La página sale en blanco** → prueba `npm run dev` en la carpeta
  `frontend` y asegúrate de que Vite dice "ready in".
- **Las imágenes no aparecen en Render** → comprueba que el commit incluye
  `media/projects/*.png` y que hiciste redeploy. Si `/media/...` da 404 con
  `DEBUG=False`, verifica que `portfolio/urls.py` sirve media con
  `django.views.static.serve` (el `static()` normal no sirve sin DEBUG).
- **El admin en español sale raro** → normal, es la traducción automática
  de Django. `LANGUAGE_CODE = 'es'` está en `settings.py`.

---

¡Disfruta construyendo y personalizando tu portfolio! 🚀
