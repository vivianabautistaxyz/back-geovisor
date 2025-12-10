from django.core.management.base import BaseCommand
from polls.models import TypeChoice

class Command(BaseCommand):
    help = 'Crea los tipos de preguntas por defecto'

    def handle(self, *args, **options):
        TypeChoice.create_default_types()
        self.stdout.write(self.style.SUCCESS('Tipos por defecto creados exitosamente'))
