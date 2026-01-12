# Implementación de Hoja de Vida en Django - Guía de Setup

## Descripción General

Se ha implementado un sistema completo de gestión de hojas de vida (CV) en tu aplicación Django con las siguientes características:

### 🎯 Funcionalidades Implementadas

1. **Modelos de Base de Datos**
   - DatosPersonales: Información personal del usuario
   - ExperienciaLaboral: Historial de empleos
   - Reconocimientos: Reconocimientos académicos y laborales
   - CursoRealizado: Cursos y capacitaciones
   - ProductoAcademico: Publicaciones y productos académicos
   - ProductoLaboral: Productos laborales realizados
   - VentaGarage: Productos en venta

2. **Funcionalidades del Usuario**
   - Ver y editar su hoja de vida
   - Agregar/modificar/eliminar secciones del CV
   - Subir certificados en PDF a Azure Storage
   - Generar y descargar CV en formato PDF
   - Visualizar CV antes de descargar

3. **Panel de Administrador**
   - Ver todas las hojas de vida
   - Acceder a hojas de vida específicas
   - Descargar CVs de usuarios
   - Administración completa en Django Admin

4. **Generación de PDF**
   - CV automático en PDF con toda la información
   - Incluye datos personales, experiencia, reconocimientos, cursos, etc.
   - Formato profesional y personalizable

5. **Integración con Azure Storage**
   - Almacenamiento de certificados en la nube
   - Configuración automática de carpetas por usuario
   - Gestión segura de documentos

## 📦 Instalación

### 1. Instalar paquetes necesarios

```bash
pip install -r requirements.txt
```

Los paquetes nuevos añadidos son:
- `azure-storage-blob==12.19.0`: Para almacenamiento en Azure
- `reportlab==4.0.7`: Para generación de PDFs
- `weasyprint==59.3`: Alternativa para PDFs más complejos

### 2. Crear las migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Crear un usuario administrador (si aún no lo has hecho)

```bash
python manage.py createsuperuser
```

### 4. Configurar variables de entorno (opcional, para Azure Storage)

Si deseas usar Azure Storage para almacenar documentos:

```bash
# En tu .env o en las variables del sistema
export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=..."
export AZURE_STORAGE_CONTAINER_NAME="certificados"
```

Si no configuras Azure Storage, los archivos se guardarán localmente en la carpeta `media/`.

### 5. Iniciar el servidor

```bash
python manage.py runserver
```

## 🗺️ URLs Disponibles

### Para Usuarios Autenticados

#### Hoja de Vida Principal
- `/hoja-vida/` - Ver mi hoja de vida
- `/hoja-vida/crear-datos-personales/` - Crear/editar datos personales

#### Experiencia Laboral
- `/hoja-vida/experiencia-laboral/crear/` - Crear experiencia
- `/hoja-vida/experiencia-laboral/<id>/editar/` - Editar experiencia
- `/hoja-vida/experiencia-laboral/<id>/eliminar/` - Eliminar experiencia

#### Reconocimientos
- `/hoja-vida/reconocimiento/crear/` - Crear reconocimiento
- `/hoja-vida/reconocimiento/<id>/editar/` - Editar reconocimiento
- `/hoja-vida/reconocimiento/<id>/eliminar/` - Eliminar reconocimiento

#### Cursos
- `/hoja-vida/curso/crear/` - Crear curso
- `/hoja-vida/curso/<id>/editar/` - Editar curso
- `/hoja-vida/curso/<id>/eliminar/` - Eliminar curso

#### Productos Académicos
- `/hoja-vida/producto-academico/crear/` - Crear producto
- `/hoja-vida/producto-academico/<id>/editar/` - Editar producto
- `/hoja-vida/producto-academico/<id>/eliminar/` - Eliminar producto

#### Productos Laborales
- `/hoja-vida/producto-laboral/crear/` - Crear producto
- `/hoja-vida/producto-laboral/<id>/editar/` - Editar producto
- `/hoja-vida/producto-laboral/<id>/eliminar/` - Eliminar producto

#### Ventas Garage
- `/hoja-vida/venta-garage/crear/` - Agregar producto
- `/hoja-vida/venta-garage/<id>/editar/` - Editar producto
- `/hoja-vida/venta-garage/<id>/eliminar/` - Eliminar producto

#### PDF
- `/hoja-vida/descargar-cv/` - Descargar CV en PDF
- `/hoja-vida/visualizar-cv/` - Ver CV en PDF en el navegador

### Para Administradores (Staff)

- `/admin-panel/hojas-vida/` - Ver todas las hojas de vida
- `/admin-panel/hoja-vida/<user_id>/` - Ver hoja de vida específica
- `/admin-panel/hoja-vida/<user_id>/descargar-cv/` - Descargar CV de un usuario
- `/admin/` - Panel administrativo Django

## 🔧 Estructura de Archivos

```
tasks/
├── models.py              # Modelos de CV
├── views_cv.py            # Vistas para gestión de CV
├── forms.py               # Formularios para CV
├── admin.py               # Configuración admin
├── azure_storage.py       # Integración con Azure
├── pdf_generator.py       # Generador de PDFs
└── templates/
    ├── cv/
    │   ├── mi_hoja_vida.html           # Vista principal del CV
    │   ├── form_datos_personales.html  # Formulario datos personales
    │   └── form_generico.html          # Formulario genérico
    └── admin/
        ├── hojas_vida.html             # Listado de hojas de vida
        └── ver_hoja_vida.html          # Ver hoja de vida (admin)
```

## 🛠️ Configuración Adicional

### Habilitar Azure Storage

En `settings.py`, ya se han añadido las siguientes variables:

```python
AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING', '')
AZURE_STORAGE_CONTAINER_NAME = os.environ.get('AZURE_STORAGE_CONTAINER_NAME', 'certificados')
```

### Personalizar estilos del PDF

El archivo `tasks/pdf_generator.py` contiene la clase `CVPDFGenerator` que puede personalizarse:

- Cambiar colores en la sección `_create_custom_styles()`
- Modificar el contenido y orden de secciones
- Ajustar márgenes y tamaños de fuente

### Personalizar formularios

Los formularios en `tasks/forms.py` pueden modificarse:

```python
# Ejemplo: cambiar atributos de un campo
'nombres': forms.TextInput(attrs={
    'class': 'tu-clase-custom',
    'placeholder': 'Tu texto'
})
```

## 🔐 Permisos y Seguridad

- Solo usuarios autenticados pueden acceder a las vistas del CV
- Solo administradores (staff) pueden acceder al panel administrativo
- Los usuarios solo pueden ver/editar su propia información
- Los archivos subidos se organizan por usuario en Azure/media

## 📝 Comandos Útiles

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ver migraciones pendientes
python manage.py showmigrations

# Revertir una migración
python manage.py migrate tasks 0001

# Crear superusuario
python manage.py createsuperuser

# Shell de Django para pruebas
python manage.py shell
```

## 🐛 Solución de Problemas

### Error: "DatosPersonales matching query does not exist"

**Solución:** El usuario debe crear su información personal primero visitando `/hoja-vida/crear-datos-personales/`

### Error: "UNIQUE constraint failed: numerocedula"

**Solución:** El número de cédula ya existe. Usa uno único o actualiza el existente.

### Error: "Azure Storage not configured"

**Solución:** Si no configuras Azure, los archivos se guardarán localmente. Configura las variables de entorno si deseas usar Azure.

### Archivos no se suben a Azure

**Solución:** Verifica que `AZURE_STORAGE_CONNECTION_STRING` sea válida. Si no está configurada, los archivos se guardarán localmente en `media/`.

## 📚 Referencias

- [Django Documentation](https://docs.djangoproject.com/)
- [ReportLab Documentation](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [Azure Storage SDK for Python](https://learn.microsoft.com/en-us/python/api/overview/azure/storage-blob-readme)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)

## 🎓 Próximos Pasos Sugeridos

1. Personalizar los estilos y colores de las plantillas
2. Agregar más campos a los formularios según tus necesidades
3. Implementar búsqueda y filtrado en el panel de admin
4. Agregar confirmación de email para usuarios
5. Crear un portal público para ver CVs (sin datos sensibles)
6. Implementar versionado de CVs
7. Agregar estadísticas y analytics

---

**¿Preguntas o mejoras?** Contacta al desarrollador.
