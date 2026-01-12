# 🚀 Configuración Rápida para Render + Azure

## Variables de Entorno para Render

Copia y pega estas variables en tu Web Service de Render (pestaña "Environment"):

### 1. SECRET_KEY
```
SECRET_KEY=<GENERA-UNA-NUEVA-AQUI>
```
**Para generar una nueva SECRET_KEY, ejecuta en Python:**
```python
import secrets
print(secrets.token_urlsafe(50))
```

### 2. PYTHON_VERSION
```
PYTHON_VERSION=3.11.0
```

### 3. AZURE_STORAGE_CONNECTION_STRING
```
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=TU_ACCOUNT;AccountKey=TU_KEY==;EndpointSuffix=core.windows.net
```
**Obtén esto desde Azure Portal:**
- Ve a tu Storage Account
- Menú → Access keys
- Copia "Connection string"

### 4. AZURE_STORAGE_CONTAINER_NAME
```
AZURE_STORAGE_CONTAINER_NAME=certificados
```

---

## Configuración en Render

### Build Command:
```bash
./build.sh
```

### Start Command:
```bash
gunicorn djangocrud.wsgi:application
```

### Environment:
- Python 3

---

## Pasos Después del Deploy

1. **Crear Superusuario:**
   - Ve al Shell de Render
   - Ejecuta: `python manage.py createsuperuser`
   
2. **Verificar:**
   - Abre tu URL: `https://tu-app.onrender.com`
   - Inicia sesión
   - Sube un certificado
   - Verifica en Azure Storage que se subió

---

## Checklist ✅

- [ ] Repository conectado a Render
- [ ] Variables de entorno configuradas
- [ ] Build command: `./build.sh`
- [ ] Start command: `gunicorn djangocrud.wsgi:application`
- [ ] Azure Storage Account creado
- [ ] Container "certificados" creado en Azure
- [ ] Connection string copiada de Azure
- [ ] Deploy iniciado
- [ ] Superusuario creado
- [ ] Aplicación funcionando

---

## 📝 Notas Importantes

- Render usa **PostgreSQL** automáticamente (no SQLite)
- Los archivos de medios se guardan en **Azure Storage**
- El primer deploy toma ~3-5 minutos
- **DEBUG=False** automáticamente en producción
- **HTTPS** habilitado automáticamente por Render

---

## 🆘 Si algo falla

1. Revisa los **Logs** en Render
2. Verifica que todas las **variables de entorno** estén correctas
3. Asegúrate que el **Connection String** de Azure sea válido
4. Verifica que el container "certificados" exista en Azure

**Documentación completa:** Ver `RENDER_DEPLOYMENT.md`
