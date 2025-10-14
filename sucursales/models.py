from django.db import models
import uuid

class Sucursal(models.Model):
    id = models.CharField(max_length=4, primary_key=True, unique=True)
    nombre = models.CharField(max_length=100, unique=True)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20, blank=True)
    email_contacto = models.EmailField(max_length=255, blank=True)
    horario = models.CharField(max_length=100, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Sucursales"
