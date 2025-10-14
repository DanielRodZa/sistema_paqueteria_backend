
from django.db import models

class Vendedor(models.Model):
    id = models.CharField(max_length=15, primary_key=True, unique=False)
    nombre = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre