from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, RecepcionistaCreateSerializer, UserSerializer
from .models import CustomUser
from operaciones.permissions import IsManagerUser, IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RecepcionistaCreateSerializer # We can reuse this or create a more generic one
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # We can use the same serializer for creation, as it handles password hashing
        return RecepcionistaCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user
        role_to_create = self.request.data.get('role', 'RECEPCIONISTA')

        # Logic for Managers
        if user.role == 'MANAGER':
            if role_to_create != 'RECEPCIONISTA':
                 raise serializers.ValidationError({"role": "Los managers solo pueden crear recepcionistas."})
            serializer.save(role='RECEPCIONISTA', sucursal=user.sucursal)
        
        # Logic for Admins
        elif user.role == 'ADMIN' or user.is_superuser:
            # Admins can create any role (Manager, Recepcionista, Admin)
            # If creating a Manager/Recepcionista, they might need to assign a branch (handled in frontend/serializer)
            # For now, we trust the input or set defaults.
            sucursal_id = self.request.data.get('sucursal')
            
            # If sucursal is passed, it should be assigned. The serializer currently doesn't expect 'sucursal' in validated_data 
            # because it's not in the fields. We might need to handle this manually or update serializer.
            
            from sucursales.models import Sucursal
            sucursal_instance = None
            if sucursal_id:
                try:
                    sucursal_instance = Sucursal.objects.get(id=sucursal_id)
                except Sucursal.DoesNotExist:
                     pass

            save_kwargs = {'role': role_to_create}
            if sucursal_instance:
                save_kwargs['sucursal'] = sucursal_instance
            
            serializer.save(**save_kwargs)
        
        else:
             raise serializers.ValidationError({"detail": "No tienes permiso para crear usuarios."})


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(is_active=True).order_by('username')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
