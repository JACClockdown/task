from django.contrib import admin
from .models import Categoria, Tarea

# Register your models here.
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'creada_en']
    search_fields = ['nombre']


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'categoria', 'estado', 'color', 'usuario', 'creada_en']
    list_filter = ['estado', 'categoria', 'creada_en']
    search_fields = ['titulo', 'descripcion']
    readonly_fields = ['color', 'creada_en', 'actualizada_en', 'finalizada_en']
