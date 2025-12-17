from rest_framework import serializers
from .models import Vendedor

class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True}
        }
        read_only_fields = ['fecha_registro']

    def validate_nombre(self, value):
        return value.upper()