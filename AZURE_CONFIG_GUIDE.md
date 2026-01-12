# Configuración de Azure Storage Blob (Opcional)

Este documento explica cómo configurar la integración con Azure Storage para almacenar certificados y documentos en la nube.

## ¿Por qué Azure Storage?

- ✓ Almacenamiento escalable en la nube
- ✓ Seguridad empresarial
- ✓ Acceso desde cualquier lugar
- ✓ Backups automáticos
- ✓ Integración con Django

## ¿Es Obligatorio?

**No.** Si no configuras Azure Storage, los archivos se guardarán localmente en la carpeta `media/` de tu proyecto.

## Instalación en Azure

### 1. Crear una Cuenta de Azure

- Visita [azure.microsoft.com](https://azure.microsoft.com)
- Crea una cuenta (incluye $200 de crédito gratuito)
- Inicia sesión en el portal

### 2. Crear una Cuenta de Almacenamiento

1. En el portal de Azure, busca "Storage accounts"
2. Click en "Create"
3. Configura:
   - **Subscription**: Tu suscripción
   - **Resource group**: Crea uno nuevo (ej: "cv-recursos")
   - **Storage account name**: Nombre único (ej: "cvappstorageblob")
   - **Region**: La más cercana a ti (ej: "East US")
   - **Performance**: Standard
   - **Redundancy**: Locally-redundant storage (LRS)
4. Click en "Review + Create"
5. Click en "Create"

### 3. Obtener la Connection String

1. Abre la cuenta de almacenamiento creada
2. En el menú izquierdo, busca "Access keys"
3. Copia la **Connection string** (debería ser algo como):
   ```
   DefaultEndpointsProtocol=https;AccountName=cvappstorageblob;AccountKey=...;EndpointSuffix=core.windows.net
   ```

### 4. Crear un Contenedor

1. En la cuenta de almacenamiento, ve a "Containers"
2. Click en "Container"
3. Nombre: `certificados`
4. Public access level: `Private`
5. Click en "Create"

## Configuración en Django

### Opción 1: Variables de Entorno (Recomendado)

#### En Windows (cmd):
```cmd
set AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
set AZURE_STORAGE_CONTAINER_NAME=certificados
```

#### En PowerShell:
```powershell
$env:AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=..."
$env:AZURE_STORAGE_CONTAINER_NAME="certificados"
```

#### En Linux/Mac:
```bash
export AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=..."
export AZURE_STORAGE_CONTAINER_NAME="certificados"
```

#### En un archivo .env (con python-dotenv):
```
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=...
AZURE_STORAGE_CONTAINER_NAME=certificados
```

```python
# En settings.py
from dotenv import load_dotenv
load_dotenv()
```

### Opción 2: Archivo de Configuración

Edita `djangocrud/settings.py`:

```python
AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=...;AccountKey=...;EndpointSuffix=core.windows.net"
AZURE_STORAGE_CONTAINER_NAME = "certificados"
```

## Uso en la Aplicación

El sistema está **automáticamente configurado**. Cuando un usuario suba un certificado:

1. Se guarda en la base de datos (modelo)
2. Se sube a Azure Storage (si está configurado)
3. Se organiza en carpetas por tipo y usuario

### Estructura en Azure

```
certificados/
├── experiencia/
│   └── username/
│       └── 1_certificado.pdf
├── reconocimientos/
│   └── username/
│       └── 2_certificado.pdf
└── cursos/
    └── username/
        └── 3_certificado.pdf
```

## Verificar que Funciona

### En Django Shell

```bash
python manage.py shell
```

```python
from tasks.azure_storage import azure_storage

# Probar conexión
result = azure_storage.upload_document(
    open('test.pdf', 'rb'),
    'test/test.pdf'
)
print(result)  # Debería imprimir la URL del archivo

# Verificar en el portal Azure → Storage account → Containers → certificados
```

## Costos

- **Primeros 12 meses**: 5 GB de almacenamiento **gratis**
- **Después**: 
  - Almacenamiento: ~$0.018/GB/mes
  - Operaciones de lectura: $0.00004/10,000 operaciones
  - Transferencia de datos: $0.08/GB (salida)

Para una aplicación pequeña (< 100 usuarios): **Muy barato**

## Troubleshooting

### "Connection refused"

- Verifica que la connection string sea correcta
- Revisa que Azure credentials sean válidas
- Prueba la conexión en Azure Portal

### "Invalid connection string"

- Copia la connection string nuevamente desde Azure Portal
- Verifica que no haya espacios extras
- Usa comillas en la terminal si hay caracteres especiales

### Files not uploaded

- Verifica que `AZURE_STORAGE_CONNECTION_STRING` esté configurado
- Revisa los logs: `python manage.py runserver` mostrará errores
- Si no está configurado, los archivos se guardarán en `media/` localmente

### "ContainerNotFound"

- Asegúrate que el contenedor "certificados" existe en Azure
- O usa un nombre diferente:
  ```python
  AZURE_STORAGE_CONTAINER_NAME = "tu-contenedor-nuevo"
  ```

## Seguridad

### Buenas Prácticas

- ✓ Nunca commits connection strings en Git
- ✓ Usa variables de entorno o .env (en .gitignore)
- ✓ Rota las claves regularmente en Azure Portal
- ✓ Usa acceso privado en contenedores
- ✓ Configura IP whitelist si es posible

### En Producción

1. Usa managed identities en Azure App Service
2. Configura role-based access control (RBAC)
3. Habilita logging y monitoreo
4. Usa Azure Key Vault para secrets

## Alternativas

Si no quieres usar Azure, también puedes:

### Google Cloud Storage
```python
# Requiere: pip install google-cloud-storage
```

### AWS S3
```python
# Requiere: pip install boto3
```

### Almacenamiento Local (Por Defecto)
- Ya funciona sin configuración
- Los archivos van a `media/` folder
- Perfecto para desarrollo

## Referencia

- [Azure Storage Documentation](https://learn.microsoft.com/en-us/azure/storage/)
- [Azure SDK Python](https://learn.microsoft.com/en-us/python/api/overview/azure/storage-blob-readme)
- [Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)

---

**¿Preguntas?** Contacta a tu equipo de soporte.
