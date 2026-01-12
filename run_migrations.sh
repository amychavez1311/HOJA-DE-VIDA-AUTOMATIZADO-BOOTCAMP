#!/bin/bash
# Script para ejecutar migraciones

echo "=========================================="
echo "Django CV Management System - Migration"
echo "=========================================="

# Crear migraciones
echo ""
echo "1. Creating migrations..."
python manage.py makemigrations tasks

# Aplicar migraciones
echo ""
echo "2. Applying migrations..."
python manage.py migrate

# Crear carpetas de media si no existen
echo ""
echo "3. Creating media directories..."
mkdir -p media/profile_pics
mkdir -p media/certificados/experiencia
mkdir -p media/certificados/reconocimientos
mkdir -p media/certificados/cursos

echo ""
echo "=========================================="
echo "✓ All migrations applied successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Create a superuser: python manage.py createsuperuser"
echo "2. Start the server: python manage.py runserver"
echo "3. Visit http://localhost:8000 to start using the application"
echo ""
