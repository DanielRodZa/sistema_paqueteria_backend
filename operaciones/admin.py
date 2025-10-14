from django.contrib import admin
from .models import Operacion

@admin.register(Operacion)
class OperacionAdmin(admin.ModelAdmin):
    list_display = ('folio', 'vendedor', 'comprador', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'tamano_paquete', 'fecha_creacion')
    search_fields = ('folio__iexact', 'vendedor__icontains', 'comprador__icontains')
