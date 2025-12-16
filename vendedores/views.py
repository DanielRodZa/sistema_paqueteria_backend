from rest_framework import generics
from .models import Vendedor
from .serializers import VendedorSerializer
from operaciones.permissions import IsAdminUser, IsAdminOrManagerUser
from rest_framework.permissions import IsAuthenticated

class VendedorListCreateView(generics.ListCreateAPIView):
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer
    
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