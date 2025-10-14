from django.core.management.base import BaseCommand
from django.utils import timezone
from operaciones.models import Operacion


class Command(BaseCommand):
    help = 'Busca operaciones no entregadas cuya fecha de expiración ya pasó y las marca como "Expirado"'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()

        operaciones_expiradas = Operacion.objects.filter(
            estado='Listo_para_entrega',
            fecha_expiracion__lte=today
        )

        count = operaciones_expiradas.update(estado='expirado')

        self.stdout.write(self.style.SUCCESS(f'Se actualizaron {count} operaciones a "Expirado".'))