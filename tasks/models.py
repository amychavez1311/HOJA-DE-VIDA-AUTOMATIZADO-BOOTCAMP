from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from datetime import date

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title +'- by '+ self.user.username


# ============================
# MODELOS PARA HOJA DE VIDA
# ============================

class DatosPersonales(models.Model):
    """Modelo para almacenar datos personales del usuario"""
    SEXO_CHOICES = [
        ('H', 'Hombre'),
        ('M', 'Mujer'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='datos_personales')
    descripcionperfil = models.CharField(max_length=50, blank=True, null=True)
    perfilactivo = models.BooleanField(default=True)
    apellidos = models.CharField(max_length=60)
    nombres = models.CharField(max_length=60)
    nacionalidad = models.CharField(max_length=20, blank=True, null=True)
    lugarnacimiento = models.CharField(max_length=60, blank=True, null=True)
    fechanacimiento = models.DateField(blank=True, null=True)
    numerocedula = models.CharField(max_length=10, unique=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True, null=True)
    estadocivil = models.CharField(max_length=50, blank=True, null=True)
    licenciaconducir = models.CharField(max_length=6, blank=True, null=True)
    telefonoconvencional = models.CharField(max_length=15, blank=True, null=True)
    telefonofijo = models.CharField(max_length=15, blank=True, null=True)
    direcciontrabajo = models.CharField(max_length=100, blank=True, null=True)
    direcciondomiciliaria = models.CharField(max_length=100, blank=True, null=True)
    sitioweb = models.CharField(max_length=60, blank=True, null=True)
    fotoperfil = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Datos Personales"
        ordering = ['-fechacreacion']

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class ExperienciaLaboral(models.Model):
    """Modelo para experiencia laboral"""
    datospersonales = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='experiencias_laborales')
    cargodesempenado = models.CharField(max_length=100)
    nombreempresa = models.CharField(max_length=100)
    lugarempresa = models.CharField(max_length=50)
    emailempresa = models.EmailField(blank=True, null=True)
    sitiowebempresa = models.URLField(blank=True, null=True)
    nombrecontactoempresarial = models.CharField(max_length=100, blank=True, null=True)
    telefonocontactoempresarial = models.CharField(max_length=60, blank=True, null=True)
    fechainiciogestion = models.DateField()
    fechafingestion = models.DateField(blank=True, null=True)
    descripcionfunciones = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    certificado = models.FileField(upload_to='certificados/experiencia/', null=True, blank=True,
                                  validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Experiencias Laborales"
        ordering = ['-fechainiciogestion']

    def __str__(self):
        return f"{self.cargodesempenado} - {self.nombreempresa}"


class Reconocimiento(models.Model):
    """Modelo para reconocimientos"""
    TIPO_CHOICES = [
        ('Académico', 'Académico'),
        ('Público', 'Público'),
        ('Privado', 'Privado'),
    ]
    
    datospersonales = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='reconocimientos')
    tiporeconocimiento = models.CharField(max_length=100, choices=TIPO_CHOICES)
    fechareconocimiento = models.DateField()
    descripcionreconocimiento = models.TextField(blank=True, null=True)
    entidadpatrocinadora = models.CharField(max_length=100)
    nombrecontactoauspicia = models.CharField(max_length=100, blank=True, null=True)
    telefonocontactoauspicia = models.CharField(max_length=60, blank=True, null=True)
    activo = models.BooleanField(default=True)
    certificado = models.FileField(upload_to='certificados/reconocimientos/', null=True, blank=True,
                                  validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Reconocimientos"
        ordering = ['-fechareconocimiento']

    def __str__(self):
        return f"{self.tiporeconocimiento} - {self.entidadpatrocinadora}"


class CursoRealizado(models.Model):
    """Modelo para cursos realizados"""
    datospersonales = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='cursos_realizados')
    nombrecurso = models.CharField(max_length=100)
    fechainicio = models.DateField()
    fechafin = models.DateField(blank=True, null=True)
    totalhoras = models.IntegerField(blank=True, null=True)
    descripcioncurso = models.TextField(blank=True, null=True)
    entidadpatrocinadora = models.CharField(max_length=100)
    nombrecontactoauspicia = models.CharField(max_length=100, blank=True, null=True)
    telefonocontactoauspicia = models.CharField(max_length=60, blank=True, null=True)
    emailempresapatrocinadora = models.EmailField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    certificado = models.FileField(upload_to='certificados/cursos/', null=True, blank=True,
                                  validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Cursos Realizados"
        ordering = ['-fechainicio']

    def __str__(self):
        return f"{self.nombrecurso} - {self.entidadpatrocinadora}"


class ProductoAcademico(models.Model):
    """Modelo para productos académicos"""
    datospersonales = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='productos_academicos')
    nombrerecurso = models.CharField(max_length=100)
    clasificador = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Productos Académicos"

    def __str__(self):
        return self.nombrerecurso


class ProductoLaboral(models.Model):
    """Modelo para productos laborales"""
    datospersonales = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='productos_laborales')
    nombreproducto = models.CharField(max_length=100)
    fechaproducto = models.DateField()
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Productos Laborales"
        ordering = ['-fechaproducto']

    def __str__(self):
        return self.nombreproducto


class VentaGarage(models.Model):
    """Modelo para productos en venta"""
    ESTADO_CHOICES = [
        ('Bueno', 'Bueno'),
        ('Regular', 'Regular'),
    ]
    
    datospersonales = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='ventas_garage')
    nombreproducto = models.CharField(max_length=100)
    estadoproducto = models.CharField(max_length=40, choices=ESTADO_CHOICES)
    descripcion = models.TextField(blank=True, null=True)
    valordelbien = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechamodificacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Ventas Garage"
        ordering = ['-fechacreacion']

    def __str__(self):
        return f"{self.nombreproducto} ({self.estadoproducto})"
