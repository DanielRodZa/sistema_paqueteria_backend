from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Configuracion
from .serializers import ConfiguracionSerializer
from operaciones.permissions import IsAdminUser

class ConfiguracionRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ConfiguracionSerializer
    serializer_class = ConfiguracionSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdminUser()]

    def get_object(self):
        obj, created = Configuracion.objects.get_or_create(pk=1)
        return obj
