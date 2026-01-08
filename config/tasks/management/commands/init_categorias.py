from django.core.management.base import BaseCommand
from tasks.models import Categoria


class Command(BaseCommand):
    help = 'Inicializa las categorías predeterminadas del sistema'

    def handle(self, *args, **kwargs):
        categorias_iniciales = [
            'Trabajo',
            'Estudio',
            'Casa',
            'Familia',
            'Diversión'
        ]
        
        creadas = 0
        existentes = 0
        
        for nombre in categorias_iniciales:
            categoria, created = Categoria.objects.get_or_create(nombre=nombre)
            if created:
                creadas += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Categoría "{nombre}" creada exitosamente')
                )
            else:
                existentes += 1
                self.stdout.write(
                    self.style.WARNING(f'- Categoría "{nombre}" ya existía')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Proceso completado: {creadas} creadas, {existentes} ya existían')
        )