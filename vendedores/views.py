from rest_framework import generics
from .models import Vendedor
from .serializers import VendedorSerializer
from operaciones.permissions import IsAdminUser, IsAdminOrManagerUser
from rest_framework.permissions import IsAuthenticated

from rest_framework import filters

class VendedorListCreateView(generics.ListCreateAPIView):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'id']
    
    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            return [IsAuthenticated()]
        return [IsAdminOrManagerUser()]


class VendedorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer

    def get_permissions(self):
        """
        Assigns permissions based on the request method.
        """
        # For GET requests, any authenticated user can view details (useful for the new operation form).
        if self.request.method == 'GET':
            return [IsAuthenticated()]

        # For any other method (PUT, PATCH, DELETE), the user must be an Admin or Manager.
        return [IsAdminOrManagerUser()]


import csv
from django.http import HttpResponse
from rest_framework.views import APIView

class VendedorExportView(APIView):
    permission_classes = [IsAdminOrManagerUser]

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="vendedores.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Nombre', 'Email', 'Telefono', 'Fecha Registro'])

        vendedores = Vendedor.objects.all()
        for v in vendedores:
            writer.writerow([v.id, v.nombre, v.email, v.telefono, v.fecha_registro])

        return response