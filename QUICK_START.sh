#!/bin/bash
# QUICK START - Guía Rápida de Inicio

echo "=========================================="
echo "Django CV System - Quick Start"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Paso 1: Instalar paquetes...${NC}"
pip install -r requirements.txt

echo -e "${YELLOW}Paso 2: Crear migraciones...${NC}"
python manage.py makemigrations tasks

echo -e "${YELLOW}Paso 3: Ejecutar migraciones...${NC}"
python manage.py migrate

echo -e "${YELLOW}Paso 4: Crear superusuario...${NC}"
python manage.py createsuperuser

echo -e "${YELLOW}Paso 5: Crear carpeta de media...${NC}"
mkdir -p media/profile_pics
mkdir -p media/certificados/experiencia
mkdir -p media/certificados/reconocimientos
mkdir -p media/certificados/cursos

echo ""
echo -e "${GREEN}=========================================="
echo "✓ Setup completado exitosamente!"
echo "==========================================${NC}"
echo ""
echo "Ahora puedes iniciar el servidor con:"
echo "  python manage.py runserver"
echo ""
echo "Y acceder a:"
echo "  http://localhost:8000/hoja-vida/"
echo ""
