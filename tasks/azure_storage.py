"""
Configuración e integración con Azure Storage Blob Service
para almacenar documentos (PDFs) de certificados
"""

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
from django.conf import settings


class AzureStorageManager:
    """Gestor para subir y descargar archivos a Azure Storage"""
    
    def __init__(self):
        self.connection_string = getattr(settings, 'AZURE_STORAGE_CONNECTION_STRING', '')
        self.container_name = getattr(settings, 'AZURE_STORAGE_CONTAINER_NAME', 'certificados')
        
    def upload_document(self, file_obj, blob_name):
        """
        Sube un archivo a Azure Storage
        
        Args:
            file_obj: Archivo a subir
            blob_name: Nombre del blob (ej: 'reconocimientos/user_123/cert.pdf')
            
        Returns:
            URL pública del archivo subido o None si falla
        """
        try:
            blob_service_client = BlobServiceClient.from_connection_string(
                self.connection_string
            )
            
            # Crear contenedor si no existe
            container_client = blob_service_client.get_container_client(self.container_name)
            try:
                container_client.get_container_properties()
            except:
                container_client = blob_service_client.create_container(self.container_name)
            
            # Subir el blob
            blob_client = blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            
            blob_client.upload_blob(file_obj, overwrite=True)
            
            # Retornar la URL del blob
            return blob_client.url
            
        except Exception as e:
            print(f"Error subiendo archivo a Azure: {str(e)}")
            return None
    
    def download_document(self, blob_name):
        """
        Descarga un archivo desde Azure Storage
        
        Args:
            blob_name: Nombre del blob a descargar
            
        Returns:
            Contenido del archivo o None si falla
        """
        try:
            blob_service_client = BlobServiceClient.from_connection_string(
                self.connection_string
            )
            blob_client = blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            
            download_stream = blob_client.download_blob()
            return download_stream.readall()
            
        except Exception as e:
            print(f"Error descargando archivo de Azure: {str(e)}")
            return None
    
    def delete_document(self, blob_name):
        """
        Elimina un archivo de Azure Storage
        
        Args:
            blob_name: Nombre del blob a eliminar
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        try:
            blob_service_client = BlobServiceClient.from_connection_string(
                self.connection_string
            )
            blob_client = blob_service_client.get_blob_client(
                container=self.container_name,
                blob=blob_name
            )
            
            blob_client.delete_blob()
            return True
            
        except Exception as e:
            print(f"Error eliminando archivo de Azure: {str(e)}")
            return False


# Instancia global del gestor
azure_storage = AzureStorageManager()
