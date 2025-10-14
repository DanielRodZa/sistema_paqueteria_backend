from rest_framework import serializers
from .models import Vendedor

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = ['id', 'nombre', 'email', 'telefono', 'fecha_registro']
        read_only_fields = ['fecha_registro']