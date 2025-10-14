from rest_framework import serializers
from .models import Operacion

class OperacionSerializer(serializers.ModelSerializer):
    vendedor_nombre = serializers.CharField(source='vendedor.nombre', read_only=True)
    sucursal_origen_nombre = serializers.CharField(source='sucursal_origen.nombre', read_only=True)
    sucursal_destino_nombre = serializers.CharField(source='sucursal_destino.nombre', read_only=True)

    class Meta:
        model = Operacion
        fields = [
            'folio',
            'vendedor',
            'vendedor_nombre',
            'comprador',
            'tamano_paquete',
            'estado',
            'sucursal_origen',
            'sucursal_destino',
            'sucursal_origen_nombre',
            'sucursal_destino_nombre',
            'costo',
            'pagado',
            'fecha_creacion',
            'fecha_actualizacion',
            'fecha_expiracion',
        ]

        read_only_fields = (
            'folio',
            'fecha_creacion',
            'fecha_actualizacion',
            'costo',
            'fecha_expiracion',
            'vendedor_nombre',
            'sucursal_origen_nombre',
            'sucursal_destino_nombre'
        )