from rest_framework import serializers
from .models import Sucursal


class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = ['id', 'nombre', 'direccion', 'telefono', 'email_contacto', 'horario', 'fecha_creacion']
        read_only_fields = ['fecha_creacion']