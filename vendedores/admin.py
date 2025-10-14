from django.contrib import admin
from .models import Vendedor

@admin.register(Vendedor)
class VendedorAdmin(admin.ModelAdmin):
    """
    Personaliza la vista del admin para el modelo Vendedor.
    """
    list_display = ('id', 'nombre', 'fecha_registro')
    search_fields = ('id', 'nombre')