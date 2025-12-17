from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import CustomUser

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Añade claims personalizados
        token['username'] = user.username
        if user.is_superuser:
            token['role'] = 'ADMIN'
        else:
            token['role'] = user.role

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom data to the response body
        data['username'] = self.user.username
        if self.user.is_superuser:
            data['role'] = 'ADMIN'
        else:
            data['role'] = self.user.role

        return data



class RecepcionistaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'telefono']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def validate_first_name(self, value):
        return value.upper()

    def validate_last_name(self, value):
        return value.upper()


class UserSerializer(serializers.ModelSerializer):
    sucursal_nombre = serializers.CharField(source='sucursal.nombre', read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'sucursal',
            'sucursal_nombre'
        ]
        read_only_fields = ['id']
