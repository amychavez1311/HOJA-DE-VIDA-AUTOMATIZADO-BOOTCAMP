"""
Vistas para la gestión de hojas de vida
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponse, FileResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db import transaction
from datetime import datetime
from functools import wraps
import os

from .models import (
    DatosPersonales, ExperienciaLaboral, Reconocimiento,
    CursoRealizado, ProductoAcademico, ProductoLaboral, VentaGarage
)
from .forms import (
    DatosPersonalesForm, ExperienciaLaboralForm, ReconocimientoForm,
    CursoRealizadoForm, ProductoAcademicoForm, ProductoLaboralForm,
    VentaGarageForm
)
from .pdf_generator import CVPDFGenerator
from .azure_storage import azure_storage


# ============================
# DECORADORES PERSONALIZADOS
# ============================

def staff_required(view_func):
    """Decorador para verificar que el usuario es staff"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para acceder a esta sección")
            return redirect('signin')
        if not request.user.is_staff:
            messages.error(request, "No tienes permisos para acceder a esta sección")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


# ============================
# VISTAS PARA USUARIOS (CV)
# ============================

@login_required
def mi_hoja_vida(request):
    """Vista principal de la hoja de vida del usuario"""
    try:
        datos = DatosPersonales.objects.get(user=request.user)
    except DatosPersonales.DoesNotExist:
        # Si no existe, redirigir a crear datos personales
        return redirect('crear_datos_personales')
    
    context = {
        'datos': datos,
        'experiencias': datos.experiencias_laborales.all(),
        'reconocimientos': datos.reconocimientos.all(),
        'cursos': datos.cursos_realizados.all(),
        'productos_academicos': datos.productos_academicos.all(),
        'productos_laborales': datos.productos_laborales.all(),
        'ventas': datos.ventas_garage.all(),
    }
    
    return render(request, 'cv/mi_hoja_vida.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def crear_datos_personales(request):
    """Vista para crear/editar datos personales"""
    try:
        datos = DatosPersonales.objects.get(user=request.user)
        is_create = False
    except DatosPersonales.DoesNotExist:
        datos = None
        is_create = True
    
    if request.method == 'POST':
        form = DatosPersonalesForm(request.POST, request.FILES, instance=datos)
        if form.is_valid():
            datos = form.save(commit=False)
            datos.user = request.user
            datos.save()
            messages.success(request, 
                'Datos personales guardados correctamente' if not is_create else 'Datos personales creados correctamente')
            return redirect('mi_hoja_vida')
        else:
            messages.error(request, 'Error en el formulario. Por favor revisa los datos.')
    else:
        form = DatosPersonalesForm(instance=datos)
    
    context = {
        'form': form,
        'titulo': 'Crear Datos Personales' if is_create else 'Editar Datos Personales',
    }
    
    return render(request, 'cv/form_datos_personales.html', context)


# ============================
# VISTAS PARA EXPERIENCIA LABORAL
# ============================

@login_required
def crear_experiencia_laboral(request):
    """Vista para crear experiencia laboral"""
    try:
        datos = DatosPersonales.objects.get(user=request.user)
    except DatosPersonales.DoesNotExist:
        messages.error(request, 'Debes crear tus datos personales primero')
        return redirect('crear_datos_personales')
    
    if request.method == 'POST':
        form = ExperienciaLaboralForm(request.POST, request.FILES)
        if form.is_valid():
            experiencia = form.save(commit=False)
            experiencia.datospersonales = datos
            experiencia.save()
            
            # Subir certificado a Azure si existe
            if experiencia.certificado:
                blob_name = f"experiencia/{datos.user.username}/{experiencia.id}_{experiencia.certificado.name}"
                azure_url = azure_storage.upload_document(
                    experiencia.certificado.open('rb'),
                    blob_name
                )
            
            messages.success(request, 'Experiencia laboral creada correctamente')
            return redirect('mi_hoja_vida')
    else:
        form = ExperienciaLaboralForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Experiencia Laboral',
        'tipo': 'experiencia_laboral'
    }
    
    return render(request, 'cv/form_generico.html', context)


@login_required
def editar_experiencia_laboral(request, id):
    """Vista para editar experiencia laboral"""
    experiencia = get_object_or_404(
        ExperienciaLaboral,
        id=id,
        datospersonales__user=request.user
    )
    
    if request.method == 'POST':
        form = ExperienciaLaboralForm(request.POST, request.FILES, instance=experiencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Experiencia laboral actualizada correctamente')
            return redirect('mi_hoja_vida')
    else:
        form = ExperienciaLaboralForm(instance=experiencia)
    
    context = {
        'form': form,
        'titulo': 'Editar Experiencia Laboral',
        'tipo': 'experiencia_laboral'
    }
    
    return render(request, 'cv/form_generico.html', context)


@login_required
@require_http_methods(["POST"])
def eliminar_experiencia_laboral(request, id):
    """Vista para eliminar experiencia laboral"""
    experiencia = get_object_or_404(
        ExperienciaLaboral,
        id=id,
        datospersonales__user=request.user
    )
    experiencia.delete()
    messages.success(request, 'Experiencia laboral eliminada correctamente')
    return redirect('mi_hoja_vida')


# ============================
# VISTAS PARA RECONOCIMIENTOS
# ============================

@login_required
def crear_reconocimiento(request):
    """Vista para crear reconocimiento"""
    try:
        datos = DatosPersonales.objects.get(user=request.user)
    except DatosPersonales.DoesNotExist:
        messages.error(request, 'Debes crear tus datos personales primero')
        return redirect('crear_datos_personales')
    
    if request.method == 'POST':
        form = ReconocimientoForm(request.POST, request.FILES)
        if form.is_valid():
            reconocimiento = form.save(commit=False)
            reconocimiento.datospersonales = datos
            reconocimiento.save()
            
            # Subir certificado a Azure si existe
            if reconocimiento.certificado:
                blob_name = f"reconocimientos/{datos.user.username}/{reconocimiento.id}_{reconocimiento.certificado.name}"
                azure_url = azure_storage.upload_document(
                    reconocimiento.certificado.open('rb'),
                    blob_name
                )
            
            messages.success(request, 'Reconocimiento creado correctamente')
            return redirect('mi_hoja_vida')
    else:
        form = ReconocimientoForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Reconocimiento',
        'tipo': 'reconocimiento'
    }
    
    return render(request, 'cv/form_generico.html', context)


@login_required
def editar_reconocimiento(request, id):
    """Vista para editar reconocimiento"""
    reconocimiento = get_object_or_404(
        Reconocimiento,
        id=id,
        datospersonales__user=request.user
    )
    
    if request.method == 'POST':
        form = ReconocimientoForm(request.POST, request.FILES, instance=reconocimiento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reconocimiento actualizado correctamente')
            return redirect('mi_hoja_vida')
    else:
        form = ReconocimientoForm(instance=reconocimiento)
    
    context = {
        'form': form,
        'titulo': 'Editar Reconocimiento',
        'tipo': 'reconocimiento'
    }
    
    return render(request, 'cv/form_generico.html', context)


@login_required
@require_http_methods(["POST"])
def eliminar_reconocimiento(request, id):
    """Vista para eliminar reconocimiento"""
    reconocimiento = get_object_or_404(
        Reconocimiento,
        id=id,
        datospersonales__user=request.user
    )
    reconocimiento.delete()
    messages.success(request, 'Reconocimiento eliminado correctamente')
    return redirect('mi_hoja_vida')


# ============================
# VISTAS PARA CURSOS
# ============================

@login_required
def crear_curso(request):
    """Vista para crear curso"""
    try:
        datos = DatosPersonales.objects.get(user=request.user)
    except DatosPersonales.DoesNotExist:
        messages.error(request, 'Debes crear tus datos personales primero')
        return redirect('crear_datos_personales')
    
    if request.method == 'POST':
        form = CursoRealizadoForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.datospersonales = datos
            curso.save()
            
            # Subir certificado a Azure si existe
            if curso.certificado:
                blob_name = f"cursos/{datos.user.username}/{curso.id}_{curso.certificado.name}"
                azure_url = azure_storage.upload_document(
                    curso.certificado.open('rb'),
                    blob_name
                )
            
            messages.success(request, 'Curso creado correctamente')
            return redirect('mi_hoja_vida')
    else:
        form = CursoRealizadoForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Curso',
        'tipo': 'curso'
    }
    
    return render(request, 'cv/form_generico.html', context)


@login_required
def editar_curso(request, id):
    """Vista para editar curso"""
    curso = get_object_or_404(
        CursoRealizado,
        id=id,
        datospersonales__user=request.user
    )
    
    if request.method == 'POST':
        form = CursoRealizadoForm(request.POST, request.FILES, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso actualizado correctamente')
            return redirect('mi_hoja_vida')
    else:
        form = CursoRealizadoForm(instance=curso)
    
    context = {
        'form': form,
        'titulo': 'Editar Curso',
        'tipo': 'curso'
    }
    
    return render(request, 'cv/form_generico.html', context)


@login_required
@require_http_methods(["POST"])
def eliminar_curso(request, id):
    """Vista para eliminar curso"""
    curso = get_object_or_404(
        CursoRealizado,
        id=id,
        datospersonales__user=request.user
    )
    curso.delete()
    messages.success(request, 'Curso eliminado correctamente')
    return redirect('mi_hoja_vida')


# ============================
# VISTAS PARA PRODUCTOS ACADÉMICOS
# ============================

@login_required
def crear_producto_academico(request):
    """Vista para crear producto académico"""
    try:
        datos = DatosPersonales.objects.get(user=request.user)
    except DatosPersonales.DoesNotExist:
        messages.error(request, 'Debes crear tus datos personales primero')
        return redirect('crear_datos_personales')
    
    if request.method == 'POST':
        form = ProductoAcademicoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.datospersonales = datos
            producto.save()
            messages.success(request, 'Producto académico creado correctamente')
            return redirect('mi_hoja_vida')
    else:
        form = ProductoAcademicoForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Producto Académico',
        'tipo': 'producto_academico'
    }
    
    return render(request, 'cv/form_generico.html', context)


@login_required
def editar_producto_academico(request, id):
    """Vista para editar producto académico"""
    producto = get_object_or_404(
        ProductoAcademico,
        id=id,
        datospersonales__user=request.user
    )
    
    if request.method == 'POST':
        form = ProductoAcademicoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto académico actualizado correctamente')
            return redirect('mi_hoja_vida')
    else:
        form = ProductoAcademicoForm(instance=producto)
    
    context = {
        'form': form,
        'titulo': 'Editar Producto Académico',
        'tipo': 'producto_academico'
    }
    
    return render(request, 'cv/form_generico.html', context)


@login_required
@require_http_methods(["POST"])
def eliminar_producto_academico(request, id):
    """Vista para eliminar producto académico"""
    producto = get_object_or_404(
        ProductoAcademico,
        id=id,
        datospersonales__user=request.user
    )
    producto.delete()
    messages.success(request, 'Producto académico eliminado correctamente')
    return redirect('mi_hoja_vida')


# ============================
# VISTAS PARA PRODUCTOS LABORALES
# ============================

@login_required
def crear_producto_laboral(request):
    """Vista para crear producto laboral"""
    try:
        datos = DatosPersonales.objects.get(user=request.user)
    except DatosPersonales.DoesNotExist:
        messages.error(request, 'Debes crear tus datos personales primero')
        return redirect('crear_datos_personales')
    
    if request.method == 'POST':
        form = ProductoLaboralForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.datospersonales = datos
            producto.save()
            messages.success(request, 'Producto laboral creado correctamente')
            return redirect('mi_hoja_vida')
    else:
        form = ProductoLaboralForm()
    
    context = {
        'form': form,
        'titulo': 'Crear Producto Laboral',
        'tipo': 'producto_laboral'
    }
    
    return render(request, 'cv/form_generico.html', context)


@login_required
def editar_producto_laboral(request, id):
    """Vista para editar producto laboral"""
    producto = get_object_or_404(
        ProductoLaboral,
        id=id,
        datospersonales__user=request.user
    )
    
    if request.method == 'POST':
        form = ProductoLaboralForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto laboral actualizado correctamente')
            return redirect('mi_hoja_vida')
    else:
        form = ProductoLaboralForm(instance=producto)
    
    context = {
        'form': form,
        'titulo': 'Editar Producto Laboral',
        'tipo': 'producto_laboral'
    }
    
    return render(request, 'cv/form_generico.html', context)


@login_required
@require_http_methods(["POST"])
def eliminar_producto_laboral(request, id):
    """Vista para eliminar producto laboral"""
    producto = get_object_or_404(
        ProductoLaboral,
        id=id,
        datospersonales__user=request.user
    )
    producto.delete()
    messages.success(request, 'Producto laboral eliminado correctamente')
    return redirect('mi_hoja_vida')


# ============================
# VISTAS PARA VENTAS GARAGE
# ============================

@login_required
def crear_venta_garage(request):
    """Vista para crear venta garage"""
    try:
        datos = DatosPersonales.objects.get(user=request.user)
    except DatosPersonales.DoesNotExist:
        messages.error(request, 'Debes crear tus datos personales primero')
        return redirect('crear_datos_personales')
    
    if request.method == 'POST':
        form = VentaGarageForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.datospersonales = datos
            venta.save()
            messages.success(request, 'Producto agregado correctamente')
            return redirect('mi_hoja_vida')
    else:
        form = VentaGarageForm()
    
    context = {
        'form': form,
        'titulo': 'Agregar Producto en Venta',
        'tipo': 'venta_garage'
    }
    
    return render(request, 'cv/form_generico.html', context)


@login_required
def editar_venta_garage(request, id):
    """Vista para editar venta garage"""
    venta = get_object_or_404(
        VentaGarage,
        id=id,
        datospersonales__user=request.user
    )
    
    if request.method == 'POST':
        form = VentaGarageForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente')
            return redirect('mi_hoja_vida')
    else:
        form = VentaGarageForm(instance=venta)
    
    context = {
        'form': form,
        'titulo': 'Editar Producto',
        'tipo': 'venta_garage'
    }
    
    return render(request, 'cv/form_generico.html', context)


@login_required
@require_http_methods(["POST"])
def eliminar_venta_garage(request, id):
    """Vista para eliminar venta garage"""
    venta = get_object_or_404(
        VentaGarage,
        id=id,
        datospersonales__user=request.user
    )
    venta.delete()
    messages.success(request, 'Producto eliminado correctamente')
    return redirect('mi_hoja_vida')


# ============================
# VISTAS PARA GENERACIÓN DE PDF
# ============================

@login_required
def descargar_cv_pdf(request):
    """Vista para descargar el CV en PDF"""
    try:
        datos = DatosPersonales.objects.get(user=request.user)
    except DatosPersonales.DoesNotExist:
        messages.error(request, 'Debes crear tu hoja de vida primero')
        return redirect('crear_datos_personales')
    
    # Generar PDF
    generator = CVPDFGenerator(datos)
    pdf_buffer = generator.generate()
    
    # Retornar como respuesta HTTP
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    filename = f"CV_{datos.user.username}_{datetime.now().strftime('%Y%m%d')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


@login_required
def visualizar_cv_pdf(request):
    """Vista para visualizar el CV en PDF en el navegador"""
    try:
        datos = DatosPersonales.objects.get(user=request.user)
    except DatosPersonales.DoesNotExist:
        messages.error(request, 'Debes crear tu hoja de vida primero')
        return redirect('crear_datos_personales')
    
    # Generar PDF
    generator = CVPDFGenerator(datos)
    pdf_buffer = generator.generate()
    
    # Retornar como respuesta HTTP
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    
    return response


# ============================
# VISTAS ADMINISTRATIVAS
# ============================

@staff_required
def admin_hojas_vida(request):
    """Vista de administrador para ver todas las hojas de vida"""
    hojas_vida = DatosPersonales.objects.all()
    
    context = {
        'hojas_vida': hojas_vida,
    }
    
    return render(request, 'admin/hojas_vida.html', context)


@staff_required
def admin_ver_hoja_vida(request, user_id):
    """Vista de administrador para ver una hoja de vida específica"""
    usuario = get_object_or_404(User, id=user_id)
    
    try:
        datos = DatosPersonales.objects.get(user=usuario)
    except DatosPersonales.DoesNotExist:
        messages.error(request, f'El usuario {usuario.username} aún no ha creado su hoja de vida')
        return redirect('admin_hojas_vida')
    
    context = {
        'datos': datos,
        'usuario': usuario,
        'experiencias': datos.experiencias_laborales.all(),
        'reconocimientos': datos.reconocimientos.all(),
        'cursos': datos.cursos_realizados.all(),
        'productos_academicos': datos.productos_academicos.all(),
        'productos_laborales': datos.productos_laborales.all(),
        'ventas': datos.ventas_garage.all(),
    }
    
    return render(request, 'admin/ver_hoja_vida.html', context)

@staff_required
def admin_descargar_cv_pdf(request, user_id):
    """Vista para que el administrador descargue el CV de un usuario"""
    usuario = get_object_or_404(User, id=user_id)
    
    try:
        datos = DatosPersonales.objects.get(user=usuario)
    except DatosPersonales.DoesNotExist:
        messages.error(request, f'El usuario {usuario.username} aún no ha creado su hoja de vida')
        return redirect('admin_hojas_vida')
    
    # Generar PDF
    generator = CVPDFGenerator(datos)
    pdf_buffer = generator.generate()
    
    # Retornar como respuesta HTTP
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    filename = f"CV_{usuario.username}_{datetime.now().strftime('%Y%m%d')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


@staff_required
def admin_editar_hoja_vida(request, user_id):
    """Vista para que el administrador edite los datos personales de un usuario"""
    usuario = get_object_or_404(User, id=user_id)
    
    try:
        datos = DatosPersonales.objects.get(user=usuario)
    except DatosPersonales.DoesNotExist:
        messages.error(request, f'El usuario {usuario.username} aún no ha creado su hoja de vida')
        return redirect('admin_hojas_vida')
    
    if request.method == 'POST':
        form = DatosPersonalesForm(request.POST, request.FILES, instance=datos)
        if form.is_valid():
            form.save()
            messages.success(request, f'Datos de {usuario.username} actualizados correctamente')
            return redirect('admin_ver_hoja_vida', user_id=usuario.id)
    else:
        form = DatosPersonalesForm(instance=datos)
    
    context = {
        'form': form,
        'usuario': usuario,
        'datos': datos,
    }
    
    return render(request, 'admin/editar_hoja_vida.html', context)

    return response
