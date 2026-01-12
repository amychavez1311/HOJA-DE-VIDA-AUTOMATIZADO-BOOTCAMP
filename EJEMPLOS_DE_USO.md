# Ejemplos de Uso del Sistema de Hojas de Vida

## 📱 Flujo de Usuario Típico

### 1. Registro e Inicio de Sesión

```
Usuario nuevo
    ↓
Visita http://localhost:8000/signup
    ↓
Completa formulario de registro
    ↓
Redirige automáticamente a /tasks
```

### 2. Crear Hoja de Vida

```
Usuario autenticado
    ↓
Navega a "Mi Hoja de Vida" → "Editar Datos Personales"
    ↓
Completa formulario:
  - Nombres: Juan
  - Apellidos: Pérez
  - Cédula: 1234567890
  - ... otros campos
    ↓
Click "Guardar Datos Personales"
    ↓
Sistema crea registro DatosPersonales
    ↓
Redirige a /hoja-vida/
```

### 3. Agregar Experiencia Laboral

```
En /hoja-vida/
    ↓
Click "Agregar" en sección "Experiencia Laboral"
    ↓
Redirige a /hoja-vida/experiencia-laboral/crear/
    ↓
Completa formulario:
  - Cargo: Ingeniero de Software
  - Empresa: TechCorp
  - Fecha Inicio: 2020-01-15
  - Fecha Fin: 2023-12-31
  - Certificado: subir PDF (opcional)
    ↓
Click "Guardar"
    ↓
Archivo sube a Azure/media (si es aplicable)
    ↓
Redirige a /hoja-vida/
    ↓
Nueva experiencia aparece en tabla
```

### 4. Editar Información

```
En /hoja-vida/
    ↓
Click en botón "Editar" (lápiz) en cualquier sección
    ↓
Redirige a formulario de edición
    ↓
Modifica campos deseados
    ↓
Click "Guardar"
    ↓
Cambios se actualizan inmediatamente
```

### 5. Eliminar Información

```
En /hoja-vida/
    ↓
Click en botón "Eliminar" (X) en cualquier sección
    ↓
Aparece confirmación "¿Estás seguro?"
    ↓
Confirma
    ↓
Registro se elimina
    ↓
Tabla se actualiza
```

### 6. Generar y Descargar CV

```
En /hoja-vida/
    ↓
Click "Descargar CV"
    ↓
Sistema:
  1. Lee DatosPersonales
  2. Obtiene todas las relaciones (experiencias, cursos, etc.)
  3. Genera PDF profesional
  4. Envía como descarga
    ↓
Archivo descargado como: CV_username_20240112.pdf
    ↓
Usuario lo puede enviar a empresas, imprimir, etc.
```

### 7. Ver CV en Navegador

```
En /hoja-vida/
    ↓
Click "Ver CV en PDF"
    ↓
Se abre PDF en navegador (preview)
    ↓
Usuario puede:
  - Revisar contenido
  - Imprimir directamente
  - Guardar como PDF local
```

## 👨‍💼 Flujo de Administrador

### Acceder al Panel

```
Admin authenticado
    ↓
Navega a "Admin" → "Hojas de Vida"
    ↓
Redirige a /admin-panel/hojas-vida/
    ↓
Ve tabla con todas las hojas de vida:
  - Usuario
  - Nombre
  - Cédula
  - Estado
  - Acciones
```

### Ver Hoja de Vida Específica

```
En listado de hojas de vida
    ↓
Click "Ver" en fila del usuario
    ↓
Redirige a /admin-panel/hoja-vida/<user_id>/
    ↓
Ve toda la información:
  - Datos personales
  - Experiencia
  - Reconocimientos
  - Cursos
  - Productos
  - Ventas
    ↓
Puede:
  - Revisar cada sección
  - Descargar CV del usuario
```

### Descargar CV de Usuario

```
En vista de hoja de vida específica
    ↓
Click "Descargar CV"
    ↓
Sistema genera PDF con datos del usuario
    ↓
Descarga como: CV_username_20240112.pdf
    ↓
Admin puede revisar, enviar, archivar
```

## 🔧 Ejemplos Técnicos

### Acceder a Datos en Shell de Django

```bash
python manage.py shell
```

```python
from tasks.models import DatosPersonales, ExperienciaLaboral
from django.contrib.auth.models import User

# Obtener datos de un usuario
user = User.objects.get(username='juan')
datos = DatosPersonales.objects.get(user=user)

# Ver información personal
print(f"Nombre: {datos.nombres} {datos.apellidos}")
print(f"Cédula: {datos.numerocedula}")
print(f"Email: {user.email}")

# Ver todas las experiencias
experiencias = datos.experiencias_laborales.all()
for exp in experiencias:
    print(f"- {exp.cargodesempenado} en {exp.nombreempresa}")

# Ver cursos activos
cursos_activos = datos.cursos_realizados.filter(activo=True)
print(f"Total cursos activos: {cursos_activos.count()}")

# Actualizar información
datos.telefonoconvencional = "555-1234"
datos.save()

print("Datos actualizados")
```

### Crear Datos de Prueba

```python
from tasks.models import DatosPersonales, ExperienciaLaboral
from django.contrib.auth.models import User
from datetime import date

# Crear usuario
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123'
)

# Crear datos personales
datos = DatosPersonales.objects.create(
    user=user,
    nombres='Test',
    apellidos='User',
    numerocedula='9876543210',
    nacionalidad='Colombian',
    sexo='H'
)

# Crear experiencia laboral
ExperienciaLaboral.objects.create(
    datospersonales=datos,
    cargodesempenado='Software Engineer',
    nombreempresa='Test Company',
    lugarempresa='Bogotá',
    fechainiciogestion=date(2022, 1, 1),
    descripcionfunciones='Development and maintenance'
)

print("Datos de prueba creados exitosamente")
```

### Generar PDF Programáticamente

```python
from tasks.models import DatosPersonales
from tasks.pdf_generator import CVPDFGenerator
from django.contrib.auth.models import User

# Obtener usuario
user = User.objects.get(username='juan')
datos = DatosPersonales.objects.get(user=user)

# Generar PDF
generator = CVPDFGenerator(datos)
pdf_buffer = generator.generate()

# Guardar a archivo
with open('cv_juan.pdf', 'wb') as f:
    f.write(pdf_buffer.getvalue())

print("PDF generado: cv_juan.pdf")
```

### Subir Archivo a Azure

```python
from tasks.azure_storage import azure_storage

# Subir documento
with open('mi_certificado.pdf', 'rb') as f:
    url = azure_storage.upload_document(
        f,
        'cursos/usuario123/certificado.pdf'
    )
    
print(f"Archivo subido a: {url}")

# Descargar documento
contenido = azure_storage.download_document(
    'cursos/usuario123/certificado.pdf'
)

# Guardar localmente
with open('descargado.pdf', 'wb') as f:
    f.write(contenido)

print("Archivo descargado")

# Eliminar documento
azure_storage.delete_document('cursos/usuario123/certificado.pdf')
print("Archivo eliminado")
```

## 🎨 Formularios de Ejemplo

### Completar Formulario de Reconocimiento

```html
Tipo de Reconocimiento: Académico
Fecha: 2023-06-15
Descripción: Certificado de Excelencia en Programación
Entidad: Universidad Nacional
Contacto: Dr. Juan Martínez
Teléfono: 555-1234
Certificado: [archivo.pdf]
Visible en CV: ✓
```

### Completar Formulario de Curso

```html
Nombre: Python Advanced
Fecha Inicio: 2023-01-10
Fecha Fin: 2023-03-20
Horas: 40
Descripción: Advanced OOP and Design Patterns
Entidad: Platzi
Contacto: support@platzi.com
Teléfono: 555-5678
Email: contact@platzi.com
Certificado: [certificado.pdf]
Visible en CV: ✓
```

## 📊 Queries Útiles

### Usuarios sin Hoja de Vida

```python
from django.contrib.auth.models import User
from tasks.models import DatosPersonales

usuarios = User.objects.filter(datos_personales__isnull=True)
print(f"Usuarios sin CV: {usuarios.count()}")
```

### Experiencias Recientes

```python
from tasks.models import ExperienciaLaboral
from datetime import timedelta
from django.utils import timezone

recientes = ExperienciaLaboral.objects.filter(
    fechacreacion__gte=timezone.now() - timedelta(days=7)
)
print(f"Experiencias creadas hace 7 días: {recientes.count()}")
```

### Cursos por Entidad

```python
from tasks.models import CursoRealizado
from django.db.models import Count

cursos = CursoRealizado.objects.values('entidadpatrocinadora').annotate(
    total=Count('id')
).order_by('-total')

for item in cursos:
    print(f"{item['entidadpatrocinadora']}: {item['total']} cursos")
```

### Valor Total en Venta

```python
from tasks.models import VentaGarage
from django.db.models import Sum

total = VentaGarage.objects.aggregate(Sum('valordelbien'))
print(f"Valor total en venta: ${total['valordelbien__sum']}")
```

## 📲 URLs Rápidas

```
Hoja de Vida: http://localhost:8000/hoja-vida/
Editar Datos: http://localhost:8000/hoja-vida/crear-datos-personales/
Ver CV: http://localhost:8000/hoja-vida/visualizar-cv/
Descargar CV: http://localhost:8000/hoja-vida/descargar-cv/
Admin CVs: http://localhost:8000/admin-panel/hojas-vida/
Admin Django: http://localhost:8000/admin/
```

## ✅ Checklist de Funcionalidades

- [ ] Usuarios pueden crear cuenta
- [ ] Usuarios pueden crear datos personales
- [ ] Usuarios pueden agregar experiencia laboral
- [ ] Usuarios pueden agregar reconocimientos
- [ ] Usuarios pueden agregar cursos
- [ ] Usuarios pueden agregar productos académicos
- [ ] Usuarios pueden agregar productos laborales
- [ ] Usuarios pueden agregar productos en venta
- [ ] Usuarios pueden editar cualquier sección
- [ ] Usuarios pueden eliminar cualquier sección
- [ ] Usuarios pueden descargar CV en PDF
- [ ] Usuarios pueden ver CV en navegador
- [ ] Administradores pueden ver todas las hojas de vida
- [ ] Administradores pueden descargar CV de cualquier usuario
- [ ] PDFs se generan correctamente
- [ ] Archivos se suben a Azure (si está configurado)
- [ ] Archivos se guardan localmente (si Azure no está configurado)

---

**¡Listo para usar!** Comienza creando tu primera hoja de vida.
