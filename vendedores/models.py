
from django.db import models

class Vendedor(models.Model):
    id = models.CharField(max_length=15, primary_key=True, unique=False)
    nombre = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            last_vendedor = Vendedor.objects.filter(id__startswith='VR').order_by('-id').first()
            if last_vendedor:
                try:
                    last_id = int(last_vendedor.id[2:])
                    new_id = f'VR{last_id + 1:04d}'
                except ValueError:
                    new_id = 'VR0001'
            else:
                new_id = 'VR0001'
            self.id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre