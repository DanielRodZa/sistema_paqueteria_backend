from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import models
from django.db.models import Count, Sum
from .models import Operacion
from .serializers import OperacionSerializer
from .filters import OperacionFilter
from .permissions import IsAdminUser, IsAdminOrManagerUser, CanMarkAsPaidPermission



class OperacionListCreateView(generics.ListCreateAPIView):
    """
    Vista para listar y crear operaciones.
    """
    serializer_class = OperacionSerializer
    filterset_class = OperacionFilter
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        sucursal_origen = serializer.validated_data.get('sucursal_origen')
        sucursal_destino = serializer.validated_data.get('sucursal_destino')

        costo = 10.00 if sucursal_origen.id == sucursal_destino.id else 20.00

        serializer.save(costo=costo)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Operacion.objects.all()
        elif user.sucursal:
            return Operacion.objects.filter(models.Q(sucursal_origen=user.sucursal) | models.Q(sucursal_destino=user.sucursal))
        return Operacion.objects.none()


class OperacionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para ver, actualizar y eliminar una operación específica.
    """
    queryset = Operacion.objects.all()
    serializer_class = OperacionSerializer
    lookup_field = 'folio'

    def get_permissions(self):
        """
        Asigna permisos basados en el método de la petición.
        """
        if self.request.method in ['PUT', 'PATCH']:
            # Para modificar, el usuario debe ser Admin/Manager O
            # (si es recepcionista) solo debe estar cambiando campos permitidos.
            return [IsAdminOrManagerUser() or CanMarkAsPaidPermission()]

        if self.request.method == 'DELETE':
            return [IsAdminOrManagerUser()]

        return [IsAuthenticated()]


class ReportesView(APIView):
    """
    Vista para generar reportes básicos.
    Solo accesible para Administradores.
    """
    permission_classes = [IsAdminOrManagerUser]

    def get(self, request, *args, **kwargs):
        user = self.request.user

        # Define the base queryset based on user role and branch
        if user.role == 'ADMIN':
            # Admins see everything
            base_queryset = Operacion.objects.all()
        elif user.sucursal:
            # CORRECTED LOGIC: Managers see operations related to their branch (origin OR destination)
            base_queryset = Operacion.objects.filter(
                models.Q(sucursal_origen=user.sucursal) | models.Q(sucursal_destino=user.sucursal)
            )
        else:
            # If a non-admin user has no branch, they see nothing
            base_queryset = Operacion.objects.none()

        # Apply date filters on top of the base queryset
        date_after = request.query_params.get('date_after', None)
        date_before = request.query_params.get('date_before', None)

        # The rest of your filtering logic is correct
        if date_after:
            base_queryset = base_queryset.filter(fecha_creacion__date__gte=date_after)
        if date_before:
            base_queryset = base_queryset.filter(fecha_creacion__date__lte=date_before)

        # Perform calculations on the final, filtered queryset
        total_operaciones_periodo = base_queryset.count()
        conteo_por_estado = base_queryset.values('estado').annotate(count=Count('folio')).order_by('estado')
        corte_de_caja = base_queryset.filter(pagado=True).aggregate(total=Sum('costo'))['total'] or 0.00

        data = {
            'total_operaciones_periodo': total_operaciones_periodo,
            'corte_de_caja': corte_de_caja,
            'conteo_por_estado': list(conteo_por_estado)
        }

        return Response(data)
