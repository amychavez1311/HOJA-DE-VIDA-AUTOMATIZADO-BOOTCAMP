# Actualizaciones del Generador de PDF

## Cambios Realizados (Enero 12, 2026)

### 1. **Imagen de Perfil en PDF** ✅
- Se agregó la capacidad de mostrar la foto de perfil del usuario en la esquina superior izquierda del CV
- La imagen se redimensiona a 1.2" x 1.2" para mantener proporciones profesionales
- Si no existe imagen de perfil, el PDF se genera sin problemas

### 2. **Secciones Dinámicas** ✅
- Solo se muestran las secciones que tienen datos cargados
- Si no hay experiencias laborales, la sección no se muestra
- Si no hay reconocimientos, la sección no se muestra
- Si no hay cursos, la sección no se muestra
- Si no hay productos académicos, la sección no se muestra
- Esto hace que el CV sea más limpio y profesional

### 3. **Mostrar Certificados en PDF** ✅
- **Reconocimientos**: Ahora muestra el nombre del archivo del certificado PDF junto a cada reconocimiento
  - Formato: "📎 Certificado adjunto: nombre_del_archivo.pdf"
  
- **Cursos Realizados**: Ahora muestra el nombre del archivo del certificado PDF junto a cada curso
  - Formato: "📎 Certificado adjunto: nombre_del_archivo.pdf"

- **Experiencia Laboral**: Los certificados ya estaban contemplados, se mantiene la funcionalidad

### 4. **Mejoras Técnicas**
- Se agregó `import Image` de reportlab.platypus para manejar imágenes
- Se agregó `import os` para validar rutas de archivos
- Se mejoró el manejo de errores al cargar imágenes
- El método `generate()` ahora valida dinámicamente qué secciones mostrar

## Código Modificado

### Archivo: `tasks/pdf_generator.py`

**Métodos Actualizados:**
1. `_add_header()` - Ahora incluye la imagen de perfil junto a los datos de contacto
2. `_add_reconocimientos()` - Ahora muestra los certificados adjuntos
3. `_add_cursos()` - Ahora muestra los certificados adjuntos
4. `generate()` - Ahora valida dinámicamente qué secciones incluir

## Ejemplos de Uso

### Para ver el CV en PDF:
1. Accede a: `http://localhost:8000/hoja-vida/`
2. Completa tu información en todas las secciones deseadas
3. Agrega certificados en Reconocimientos y Cursos
4. Descarga el PDF utilizando el botón "Descargar CV"

### Estructura del CV Generado:
```
┌─────────────────────────────────────┐
│ [FOTO] NOMBRE COMPLETO              │
│        Profesión/Perfil             │
│        Teléfono, Email, Sitio Web   │
└─────────────────────────────────────┘

DATOS PERSONALES
- Cédula, Sexo, Fecha Nacimiento, etc.

EXPERIENCIA LABORAL (si existe)
- Cargo, Empresa, Fechas, Descripción
- 📎 Certificado adjunto: archivo.pdf

RECONOCIMIENTOS (si existe)
- Tipo, Entidad, Fecha
- 📎 Certificado adjunto: archivo.pdf

CURSOS Y CAPACITACIONES (si existe)
- Nombre, Entidad, Fechas, Horas
- 📎 Certificado adjunto: archivo.pdf

PRODUCTOS ACADÉMICOS (si existe)
- Nombre, Clasificador, Descripción
```

## Notas Importantes

- Los certificados se enumeran por su nombre de archivo en el PDF
- Los archivos PDF adjuntos NO se incrustan en el PDF (esto requeriría una librería adicional)
- Los nombres de los archivos aparecen como referencia para imprimir/descargar posteriormente
- Si deseas incluir los PDFs incrustados, se recomienda usar WeasyPrint en lugar de ReportLab (requiere cambios adicionales)

## Estado Actual ✅

- ✅ Sistema completamente funcional
- ✅ Todos los cambios se han aplicado correctamente
- ✅ Servidor Django reloaded automáticamente
- ✅ Listo para descargar CVs con las nuevas características
