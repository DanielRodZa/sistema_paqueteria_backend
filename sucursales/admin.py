from django.contrib import admin
from .models import Sucursal

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    """
    Personaliza la vista del admin para el modelo Sucursal.
    """
    list_display = ('id', 'nombre', 'direccion', 'telefono')
    search_fields = ('id', 'nombre')
