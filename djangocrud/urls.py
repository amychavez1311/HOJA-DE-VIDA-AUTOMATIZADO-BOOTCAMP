"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from tasks import views_cv
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('signup/',views.signup,name='signup'),
    path('tasks/',views.tasks,name='tasks'),
    path('tasks_completed/',views.tasks_completed,name='tasks_completed'),
    path('tasks/create/',views.create_task,name='create_task'),
    path('tasks/<int:task_id>/',views.task_detail,name='task_detail'),
    path('tasks/<int:task_id>/complete',views.complete_task,name='complete_task'),
    path('tasks/<int:task_id>/delete',views.delete_task,name='delete_task'),
    path('logout/',views.signout,name='logout'),
    path('signin/',views.signin,name='signin'),
    
    # URLs para Hoja de Vida
    path('hoja-vida/', views_cv.mi_hoja_vida, name='mi_hoja_vida'),
    path('hoja-vida/crear-datos-personales/', views_cv.crear_datos_personales, name='crear_datos_personales'),
    
    # URLs para Experiencia Laboral
    path('hoja-vida/experiencia-laboral/crear/', views_cv.crear_experiencia_laboral, name='crear_experiencia_laboral'),
    path('hoja-vida/experiencia-laboral/<int:id>/editar/', views_cv.editar_experiencia_laboral, name='editar_experiencia_laboral'),
    path('hoja-vida/experiencia-laboral/<int:id>/eliminar/', views_cv.eliminar_experiencia_laboral, name='eliminar_experiencia_laboral'),
    
    # URLs para Reconocimientos
    path('hoja-vida/reconocimiento/crear/', views_cv.crear_reconocimiento, name='crear_reconocimiento'),
    path('hoja-vida/reconocimiento/<int:id>/editar/', views_cv.editar_reconocimiento, name='editar_reconocimiento'),
    path('hoja-vida/reconocimiento/<int:id>/eliminar/', views_cv.eliminar_reconocimiento, name='eliminar_reconocimiento'),
    
    # URLs para Cursos
    path('hoja-vida/curso/crear/', views_cv.crear_curso, name='crear_curso'),
    path('hoja-vida/curso/<int:id>/editar/', views_cv.editar_curso, name='editar_curso'),
    path('hoja-vida/curso/<int:id>/eliminar/', views_cv.eliminar_curso, name='eliminar_curso'),
    
    # URLs para Productos Académicos
    path('hoja-vida/producto-academico/crear/', views_cv.crear_producto_academico, name='crear_producto_academico'),
    path('hoja-vida/producto-academico/<int:id>/editar/', views_cv.editar_producto_academico, name='editar_producto_academico'),
    path('hoja-vida/producto-academico/<int:id>/eliminar/', views_cv.eliminar_producto_academico, name='eliminar_producto_academico'),
    
    # URLs para Productos Laborales
    path('hoja-vida/producto-laboral/crear/', views_cv.crear_producto_laboral, name='crear_producto_laboral'),
    path('hoja-vida/producto-laboral/<int:id>/editar/', views_cv.editar_producto_laboral, name='editar_producto_laboral'),
    path('hoja-vida/producto-laboral/<int:id>/eliminar/', views_cv.eliminar_producto_laboral, name='eliminar_producto_laboral'),
    
    # URLs para Ventas Garage
    path('hoja-vida/venta-garage/crear/', views_cv.crear_venta_garage, name='crear_venta_garage'),
    path('hoja-vida/venta-garage/<int:id>/editar/', views_cv.editar_venta_garage, name='editar_venta_garage'),
    path('hoja-vida/venta-garage/<int:id>/eliminar/', views_cv.eliminar_venta_garage, name='eliminar_venta_garage'),
    
    # URLs para PDF
    path('hoja-vida/descargar-cv/', views_cv.descargar_cv_pdf, name='descargar_cv_pdf'),
    path('hoja-vida/visualizar-cv/', views_cv.visualizar_cv_pdf, name='visualizar_cv_pdf'),
    
    # URLs Administrativas
    path('admin-panel/hojas-vida/', views_cv.admin_hojas_vida, name='admin_hojas_vida'),
    path('admin-panel/hoja-vida/<int:user_id>/', views_cv.admin_ver_hoja_vida, name='admin_ver_hoja_vida'),
    path('admin-panel/hoja-vida/<int:user_id>/editar/', views_cv.admin_editar_hoja_vida, name='admin_editar_hoja_vida'),
    path('admin-panel/hoja-vida/<int:user_id>/descargar-cv/', views_cv.admin_descargar_cv_pdf, name='admin_descargar_cv_pdf'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

