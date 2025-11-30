from django.db import models

class Configuracion(models.Model):
    # Singleton pattern: only one instance allowed
    costo_operacion_base = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    costo_envio_sucursal = models.DecimalField(max_digits=10, decimal_places=2, default=20.00)
    costo_extra_largo = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    costo_urgente = models.DecimalField(max_digits=10, decimal_places=2, default=30.00)
    costo_retraso_mensual = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)

    def save(self, *args, **kwargs):
        if not self.pk and Configuracion.objects.exists():
            # If you try to create a new one, it updates the existing one
            return Configuracion.objects.first()
        return super(Configuracion, self).save(*args, **kwargs)

    def __str__(self):
        return "Configuración Global"

    class Meta:
        verbose_name = "Configuración"
        verbose_name_plural = "Configuración"
