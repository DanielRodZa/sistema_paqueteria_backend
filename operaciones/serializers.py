from rest_framework import serializers
from .models import Operacion

class OperacionSerializer(serializers.ModelSerializer):
    vendedor_nombre = serializers.CharField(source='vendedor.nombre', read_only=True)
    sucursal_origen_nombre = serializers.CharField(source='sucursal_origen.nombre', read_only=True)
    sucursal_destino_nombre = serializers.CharField(source='sucursal_destino.nombre', read_only=True)
    recibido_por_nombre = serializers.CharField(source='recibido_por.username', read_only=True)
    entregado_por_nombre = serializers.CharField(source='entregado_por.username', read_only=True)

    costo_con_penalizacion = serializers.SerializerMethodField()

    class Meta:
        model = Operacion
        fields = [
            'folio',
            'vendedor',
            'vendedor_nombre',
            'comprador',
            'tamano_paquete',
            'peso',
            'tipo_entrega',
            'estado',
            'sucursal_origen',
            'sucursal_destino',
            'sucursal_origen_nombre',
            'sucursal_destino_nombre',
            'costo',
            'costo_con_penalizacion',
            'pagado',
            'recibido_por',
            'entregado_por',
            'recibido_por_nombre',
            'entregado_por_nombre',
            'fecha_creacion',
            'fecha_actualizacion',
            'fecha_expiracion',
        ]

        read_only_fields = (
            'folio',
            'fecha_creacion',
            'fecha_actualizacion',
            'costo',
            'costo_con_penalizacion',
            'fecha_expiracion',
            'vendedor_nombre',
            'sucursal_origen_nombre',
            'sucursal_destino_nombre',
            'recibido_por_nombre',
            'entregado_por_nombre'
        )

    def get_costo_con_penalizacion(self, obj):
        from django.utils import timezone
        from configuracion.models import Configuracion
        
        total_cost = obj.costo
        
        if obj.fecha_expiracion and obj.fecha_expiracion < timezone.now().date():
            # Calculate months expired
            today = timezone.now().date()
            delta = today - obj.fecha_expiracion
            # Approximate months (30 days)
            months_overdue = (delta.days // 30) + 1 # Charge for the started month
            
            config = Configuracion.objects.first()
            if config:
                penalty = config.costo_retraso_mensual * months_overdue
                total_cost += penalty
        
        return total_cost