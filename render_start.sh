#!/usr/bin/env bash
# Script de arranque para Render.
# Se ejecuta en cada boot del servicio (el disco de Render es efímero,
# así que hay que migrar y cargar los datos en cada arranque).
set -e

echo "==> Aplicando migraciones..."
python manage.py migrate --noinput

echo "==> Cargando contenido (seed)..."
python manage.py seed

echo "==> Arrancando gunicorn..."
python -m gunicorn portfolio.wsgi:application
