# 📊 VISUALIZACIÓN DEL SISTEMA IMPLEMENTADO

## 🗂️ Estructura de la Base de Datos

```
┌─────────────────────────────────────────────────────────────┐
│                    DATOSPERSONALES (Usuario)               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ • nombres, apellidos, cédula                        │  │
│  │ • fechanacimiento, nacionalidad, sexo               │  │
│  │ • contactos (teléfono, email, web)                  │  │
│  │ • direcciones                                        │  │
│  │ • fotoperfil                                         │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
        │
        ├─→ ExperienciaLaboral (1 a N)
        │   ├─ cargodesempenado
        │   ├─ nombreempresa
        │   ├─ fechainiciogestion / fechafingestion
        │   ├─ descripcionfunciones
        │   └─ certificado (PDF)
        │
        ├─→ Reconocimiento (1 a N)
        │   ├─ tiporeconocimiento (Académico/Público/Privado)
        │   ├─ entidadpatrocinadora
        │   ├─ fechareconocimiento
        │   ├─ descripcionreconocimiento
        │   └─ certificado (PDF)
        │
        ├─→ CursoRealizado (1 a N)
        │   ├─ nombrecurso
        │   ├─ fechainicio / fechafin
        │   ├─ totalhoras
        │   ├─ entidadpatrocinadora
        │   ├─ descripcioncurso
        │   └─ certificado (PDF)
        │
        ├─→ ProductoAcademico (1 a N)
        │   ├─ nombrerecurso
        │   ├─ clasificador
        │   └─ descripcion
        │
        ├─→ ProductoLaboral (1 a N)
        │   ├─ nombreproducto
        │   ├─ fechaproducto
        │   └─ descripcion
        │
        └─→ VentaGarage (1 a N)
            ├─ nombreproducto
            ├─ estadoproducto (Bueno/Regular)
            ├─ valordelbien
            └─ descripcion
```

## 🌐 Flujo de Navegación

```
                    ┌─────────────────┐
                    │  Inicio (Home)  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Login/Signup   │
                    └────────┬────────┘
                             │
                    ┌────────▼──────────────┐
                    │ Panel de Usuario      │
                    │  (Dashboard)          │
                    └────────┬──────────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
      ┌─────▼────┐  ┌──────▼────────┐ ┌────▼────────┐
      │ Datos    │  │ Agregar:      │ │ Descargar   │
      │Personal  │  │ - Experiencia │ │ CV en PDF   │
      │          │  │ - Cursos      │ │             │
      │ Editar   │  │ - Reconocos   │ │ Ver Preview │
      │          │  │ - Productos   │ │             │
      │ Eliminar │  │               │ │ Administrador
      └──────────┘  └───────────────┘ └─────────────┘
```

## 🔐 Control de Acceso

```
                  ┌──────────────────┐
                  │  Usuario Normal  │
                  └────────┬─────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
      ┌─────▼────┐ ┌───────▼──────┐ ┌────▼────────┐
      │ Ver CV   │ │ Editar CV    │ │ Descargar   │
      │ Propio   │ │ Propio       │ │ CV Propio   │
      │ ✓        │ │ ✓            │ │ ✓           │
      │ ✗ Otros  │ │ ✗ Otros      │ │ ✗ Otros     │
      └──────────┘ └──────────────┘ └─────────────┘

                  ┌──────────────────┐
                  │  Usuario Admin   │
                  └────────┬─────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
      ┌─────▼────────┐ ┌──▼──────────┐ ┌─▼───────────┐
      │ Ver todos    │ │ Acceso Total│ │ Descargar   │
      │ los CVs      │ │ a datos     │ │ cualquier   │
      │ ✓            │ │ ✓           │ │ CV          │
      │              │ │             │ │ ✓           │
      └──────────────┘ └─────────────┘ └─────────────┘
```

## 📱 Interfaz de Usuario

```
┌────────────────────────────────────────────────────────┐
│                    NAVBAR                             │
│  Home | Tasks | Mi Hoja de Vida ▼ | Admin ▼ | Logout │
└────────────────────────────────────────────────────────┘
│
├─ Mi Hoja de Vida ▼
│  ├─ Ver Mi CV
│  ├─ Editar Datos Personales
│  └─ Descargar CV
│
└─ Admin ▼
   ├─ Hojas de Vida
   └─ Panel Django Admin

┌─────────────────────────────────────────────────────────┐
│               MI HOJA DE VIDA (Dashboard)              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  DATOS PERSONALES                             [Editar] │
│  ├─ Nombre: Juan Pérez                                │
│  ├─ Cédula: 1234567890                               │
│  ├─ Email: juan@example.com                          │
│  └─ ...                                               │
│                                                       │
│  EXPERIENCIA LABORAL                      [+ Agregar] │
│  ├─ Ingeniero de Software - TechCorp       [✎ ✗]     │
│  ├─ Desarrollador Junior - StartUp         [✎ ✗]     │
│  └─ ...                                               │
│                                                       │
│  RECONOCIMIENTOS                          [+ Agregar] │
│  ├─ Certificado de Excelencia - 2023       [✎ ✗]     │
│  └─ ...                                               │
│                                                       │
│  CURSOS Y CAPACITACIONES                  [+ Agregar] │
│  ├─ Python Advanced - Platzi                [✎ ✗]    │
│  └─ ...                                               │
│                                                       │
│  [Ver CV en PDF] [Descargar CV]                       │
│                                                       │
└─────────────────────────────────────────────────────────┘
```

## 📄 Generación de PDF

```
DatosPersonales + Relacionados
        │
        ▼
CVPDFGenerator.generate()
        │
        ├─ Datos Personales (encabezado)
        ├─ Información de contacto
        ├─ Experiencia Laboral
        ├─ Reconocimientos
        ├─ Cursos y Capacitaciones
        ├─ Productos Académicos
        ├─ Productos Laborales
        └─ Pie de página
        │
        ▼
PDF BytesIO Buffer
        │
        ├─ Descargar (attachment)
        └─ Visualizar (inline)
```

## 🔄 Ciclo de Vida de Datos

```
USUARIO CREA DATOS
        │
        ▼
FORMULARIO VALIDA
        │
        ▼
MODELO GUARDA EN BD
        │
        ├─ Si es archivo → Sube a Azure/Local
        │
        ▼
USUARIO PUEDE:
        ├─ Editar (vuelve al formulario)
        ├─ Eliminar (confirmación)
        └─ Ver en CV (PDF)
        │
        ▼
GENERAR PDF
        │
        └─ Descargar o ver en navegador
```

## 🗄️ Almacenamiento de Archivos

### Local (Sin Azure)
```
media/
├── profile_pics/
│   └── user123_profile.jpg
└── certificados/
    ├── experiencia/
    │   └── user123/cert1.pdf
    ├── reconocimientos/
    │   └── user123/cert2.pdf
    └── cursos/
        └── user123/cert3.pdf
```

### Azure Storage
```
certificados/ (container)
├── experiencia/
│   └── user123/123_cert.pdf
├── reconocimientos/
│   └── user123/456_cert.pdf
└── cursos/
    └── user123/789_cert.pdf
```

## 📊 Estadísticas de Implementación

```
MODELOS
┌─────────────┬──────────────┐
│ Nombre      │ Relaciones   │
├─────────────┼──────────────┤
│ Personal    │ 1:N a 6 otras│
│ Experiencia │ N:1          │
│ Recono.     │ N:1          │
│ Cursos      │ N:1          │
│ Prod. Acad. │ N:1          │
│ Prod. Lab.  │ N:1          │
│ Venta       │ N:1          │
└─────────────┴──────────────┘
Total: 7 modelos, 6 relaciones

VISTAS
┌──────────────┬─────────┐
│ Tipo         │ Cantidad│
├──────────────┼─────────┤
│ CRUD Usuario │ 28      │
│ Admin        │ 3       │
│ PDF          │ 2       │
│ Otros        │ 7       │
└──────────────┴─────────┘
Total: 40+ vistas

FORMULARIOS
┌──────────────┬──────────┐
│ Nombre       │ Campos   │
├──────────────┼──────────┤
│ DatosPersonales│   13    │
│ Experiencia    │   12    │
│ Reconocimiento │    9    │
│ Curso          │   11    │
│ Prod. Acad.    │    4    │
│ Prod. Lab.     │    4    │
│ Venta          │    5    │
└──────────────┴──────────┘
Total: 7 formularios, 58 campos
```

## 🎨 Stack Tecnológico

```
FRONTEND
├─ HTML5
├─ Bootstrap 5
├─ Bootstrap Icons
└─ CSS personalizado

BACKEND
├─ Django 4.2
├─ Python 3.8+
├─ ORM Django
└─ Django Forms

BASE DE DATOS
├─ SQLite (desarrollo)
└─ PostgreSQL (producción)

GENERACIÓN
├─ ReportLab (PDF)
└─ Pillow (Imágenes)

ALMACENAMIENTO
├─ Sistema de archivos
└─ Azure Blob Storage (opcional)

AUTENTICACIÓN
├─ Django Auth
└─ Decoradores personalizados
```

## 📈 Escalabilidad

```
Usuarios                 Ilimitados
│
├─ Datos Personales     1:1
├─ Experiencias         1:N (sin límite)
├─ Reconocimientos      1:N (sin límite)
├─ Cursos               1:N (sin límite)
├─ Productos Académicos 1:N (sin límite)
├─ Productos Laborales  1:N (sin límite)
└─ Ventas               1:N (sin límite)

Almacenamiento
├─ Local: Hasta capacidad de disco
└─ Azure: Hasta 500TB por cuenta
```

## 🔐 Capas de Seguridad

```
SOLICITUD HTTP
        │
        ▼
MIDDLEWARE CSRF ✓
        │
        ▼
AUTENTICACIÓN (@login_required) ✓
        │
        ▼
AUTORIZACIÓN (solo datos propios) ✓
        │
        ▼
VALIDACIÓN (formularios Django) ✓
        │
        ▼
BASE DE DATOS (ORM seguro) ✓
        │
        ▼
RESPUESTA HTTP
```

---

**Visualización completa del sistema implementado** ✓
