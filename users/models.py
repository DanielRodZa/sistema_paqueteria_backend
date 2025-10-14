from django.db import models
from django.contrib.auth.models import AbstractUser

from sucursales.models import Sucursal


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Manager"
        RECEPCIONISTA = "RECEPCIONISTA", "Recepcionista"

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.RECEPCIONISTA)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT, null=True, blank=True)
    telefono = models.CharField(max_length=20, blank=True)