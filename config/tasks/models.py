from django.db import models
from django.contrib.auth.models import User
import random


def generar_color_unico():
    """Genera un color hexadecimal aleatorio"""
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    creada_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categorias"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Tarea(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('finalizada', 'Finalizada'),
    ]
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='tareas')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    color = models.CharField(max_length=7, editable=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tareas')
    creada_en = models.DateTimeField(auto_now_add=True)
    actualizada_en = models.DateTimeField(auto_now=True)
    finalizada_en = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-creada_en']
        indexes = [
            models.Index(fields=['usuario', 'estado']),
            models.Index(fields=['-creada_en']),
        ]
    
    def __str__(self):
        return f"{self.titulo} - {self.estado}"
    
    def save(self, *args, **kwargs):
        if not self.color:
            
            while True:
                nuevo_color = generar_color_unico()
                if not Tarea.objects.filter(usuario=self.usuario, color=nuevo_color).exists():
                    self.color = nuevo_color
                    break
        super().save(*args, **kwargs)