from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, RecepcionistaCreateSerializer, UserSerializer
from .models import CustomUser
from operaciones.permissions import IsManagerUser, IsAdminUser


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RecepcionistaCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RecepcionistaCreateSerializer
    permission_classes = [IsManagerUser]

    def perform_create(self, serializer):
        """
        Asigna automáticamente el rol y la sucursal del manager que está creando el usuario.
        """
        manager = self.request.user
        serializer.save(role='RECEPCIONISTA', sucursal=manager.sucursal)


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
