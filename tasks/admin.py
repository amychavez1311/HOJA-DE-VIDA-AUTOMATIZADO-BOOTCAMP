from django.contrib import admin
from .models import (
    Task, DatosPersonales, ExperienciaLaboral, Reconocimiento,
    CursoRealizado, ProductoAcademico, ProductoLaboral, VentaGarage
)


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", )


class DatosPersonalesAdmin(admin.ModelAdmin):
    readonly_fields = ("fechacreacion", "fechamodificacion")
    list_display = ("nombres", "apellidos", "numerocedula", "perfilactivo")
    search_fields = ("nombres", "apellidos", "numerocedula")
    list_filter = ("perfilactivo", "sexo")


class ExperienciaLaboralAdmin(admin.ModelAdmin):
    readonly_fields = ("fechacreacion", "fechamodificacion")
    list_display = ("cargodesempenado", "nombreempresa", "datospersonales", "activo")
    search_fields = ("cargodesempenado", "nombreempresa")
    list_filter = ("activo", "fechainiciogestion")


class ReconocimientoAdmin(admin.ModelAdmin):
    readonly_fields = ("fechacreacion", "fechamodificacion")
    list_display = ("tiporeconocimiento", "entidadpatrocinadora", "datospersonales", "activo")
    search_fields = ("tiporeconocimiento", "entidadpatrocinadora")
    list_filter = ("tiporeconocimiento", "activo", "fechareconocimiento")


class CursoRealizadoAdmin(admin.ModelAdmin):
    readonly_fields = ("fechacreacion", "fechamodificacion")
    list_display = ("nombrecurso", "entidadpatrocinadora", "datospersonales", "activo")
    search_fields = ("nombrecurso", "entidadpatrocinadora")
    list_filter = ("activo", "fechainicio")


class ProductoAcademicoAdmin(admin.ModelAdmin):
    readonly_fields = ("fechacreacion", "fechamodificacion")
    list_display = ("nombrerecurso", "clasificador", "datospersonales", "activo")
    search_fields = ("nombrerecurso", "clasificador")
    list_filter = ("activo",)


class ProductoLaboralAdmin(admin.ModelAdmin):
    readonly_fields = ("fechacreacion", "fechamodificacion")
    list_display = ("nombreproducto", "fechaproducto", "datospersonales", "activo")
    search_fields = ("nombreproducto",)
    list_filter = ("activo", "fechaproducto")


class VentaGarageAdmin(admin.ModelAdmin):
    readonly_fields = ("fechacreacion", "fechamodificacion")
    list_display = ("nombreproducto", "estadoproducto", "valordelbien", "datospersonales", "activo")
    search_fields = ("nombreproducto",)
    list_filter = ("estadoproducto", "activo")


admin.site.register(Task, TaskAdmin)
admin.site.register(DatosPersonales, DatosPersonalesAdmin)
admin.site.register(ExperienciaLaboral, ExperienciaLaboralAdmin)
admin.site.register(Reconocimiento, ReconocimientoAdmin)
admin.site.register(CursoRealizado, CursoRealizadoAdmin)
admin.site.register(ProductoAcademico, ProductoAcademicoAdmin)
admin.site.register(ProductoLaboral, ProductoLaboralAdmin)
admin.site.register(VentaGarage, VentaGarageAdmin)

