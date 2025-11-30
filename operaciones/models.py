import uuid
from django.db import models, transaction
from django.db.models import Max
from django.utils import timezone
from datetime import timedelta
from sucursales.models import Sucursal
from vendedores.models import Vendedor
from django.conf import settings

class Operacion(models.Model):
    class Tamanos(models.TextChoices):
        CHICO = 'CH', 'Chico'
        MEDIANO = 'M', 'Mediano'
        GRANDE = 'G', 'Grande'
        EXTRA_LARGO = 'XL', 'Extra Largo'

    class Estados(models.TextChoices):
        LISTO_PARA_ENTREGA = 'listo_para_entrega', 'Listo para entrega'
        EN_RESGUARDO = 'en_resguardo', 'En resguardo (Tiempo excedido)'
        EN_TRANSITO = 'en_transito', 'En tránsito'
        ENTREGADO = 'entregado', 'Entregado a comprador'
        CANCELADO = 'cancelado', 'Cancelado'
        EXPIRADO = 'expirado', 'Expirado'

    class TipoEntrega(models.TextChoices):
        NORMAL = 'normal', 'Normal'
        URGENTE = 'urgente', 'Urgente'

    folio = models.CharField(max_length=25, primary_key=True, unique=True)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.PROTECT, related_name='operaciones')
    comprador = models.CharField(max_length=255, blank=False, null=False)
    tamano_paquete = models.CharField(max_length=2, choices=Tamanos.choices, default=Tamanos.CHICO)
    peso = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    tipo_entrega = models.CharField(max_length=10, choices=TipoEntrega.choices, default=TipoEntrega.NORMAL)

    sucursal_origen = models.ForeignKey(Sucursal, on_delete=models.PROTECT, related_name='operaciones_origen')
    sucursal_destino = models.ForeignKey(Sucursal, on_delete=models.PROTECT, related_name='operaciones_destino')

    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pagado = models.BooleanField(default=False)

    estado = models.CharField(max_length=20, choices=Estados.choices, default=Estados.LISTO_PARA_ENTREGA)
    
    recibido_por = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='operaciones_recibidas', on_delete=models.SET_NULL, null=True, blank=True)
    entregado_por = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='operaciones_entregadas', on_delete=models.SET_NULL, null=True, blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    fecha_expiracion = models.DateField(editable=False, null=True)

    def __str__(self):
        return f"{self.folio} - {self.vendedor} -> {self.comprador}"

    def save(self, *args, **kwargs):
        if not self.folio:
            with transaction.atomic():
                prefix = self.sucursal_origen.id.upper()
                today = timezone.now().date()
                date_str = today.strftime('%Y%m%d')
                size_str = self.tamano_paquete
                
                # Folio format: SUC-DATE-SIZE-SEQ (e.g., SUC1-20231027-XL-001)
                base_folio = f'{prefix}-{date_str}-{size_str}-'
                
                current_day_folios = Operacion.objects.filter(folio__startswith=base_folio).select_for_update()
                
                max_folio = current_day_folios.aggregate(max_folio=Max('folio'))['max_folio']

                if max_folio:
                    try:
                        last_sequence = int(max_folio.split('-')[-1])
                        new_sequence = last_sequence + 1
                    except ValueError:
                        new_sequence = 1
                else:
                    new_sequence = 1

                self.folio = f'{base_folio}{new_sequence:03d}'

                # La lógica de la fecha de expiración no cambia
                if not self.fecha_expiracion:
                    self.fecha_expiracion = (timezone.now() + timedelta(days=30)).date()
                
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Operación"
        verbose_name_plural = "Operaciones"
        ordering = ['-fecha_creacion']