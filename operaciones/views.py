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



from configuracion.models import Configuracion

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
        tamano_paquete = serializer.validated_data.get('tamano_paquete')

        # Get configuration or use defaults
        config = Configuracion.objects.first()
        if not config:
            config = Configuracion.objects.create()

        # Base cost
        if sucursal_origen.id == sucursal_destino.id:
            costo = config.costo_operacion_base
        else:
            costo = config.costo_envio_sucursal

        # Extra cost for Extra Large
        if tamano_paquete == 'XL':
            costo += config.costo_extra_largo

        # Extra cost for Urgent delivery
        tipo_entrega = serializer.validated_data.get('tipo_entrega')
        if tipo_entrega == 'urgente':
            costo += config.costo_urgente

        serializer.save(costo=costo, recibido_por=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN' or user.is_superuser:
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

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN' or user.is_superuser:
            return Operacion.objects.all()
        elif user.sucursal:
            return Operacion.objects.filter(models.Q(sucursal_origen=user.sucursal) | models.Q(sucursal_destino=user.sucursal))
        return Operacion.objects.none()

    def get_permissions(self):
        """
        Asigna permisos basados en el método de la petición.
        """
        if self.request.method in ['PUT', 'PATCH']:
            # Para modificar, el usuario debe ser Admin/Manager O
            # (si es recepcionista) solo debe estar cambiando campos permitidos.
            return [(IsAdminOrManagerUser | CanMarkAsPaidPermission)()]

        if self.request.method == 'DELETE':
            return [IsAdminOrManagerUser()]

        return [IsAuthenticated()]

    def perform_update(self, serializer):
        instance = self.get_object()
        new_estado = serializer.validated_data.get('estado')

        if new_estado == 'entregado' and instance.estado != 'entregado':
            serializer.save(entregado_por=self.request.user)
        else:
            serializer.save()


class ReportesView(APIView):
    """
    Vista para generar reportes básicos.
    Solo accesible para Administradores.
    """
    permission_classes = [IsAdminOrManagerUser]

    def get(self, request, *args, **kwargs):
        user = self.request.user

        # Define the base queryset based on user role and branch
        if user.role == 'ADMIN' or user.is_superuser:
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
        vendedor_query = request.query_params.get('vendedor', None)

        # The rest of your filtering logic is correct
        if date_after:
            base_queryset = base_queryset.filter(fecha_creacion__date__gte=date_after)
        if date_before:
            base_queryset = base_queryset.filter(fecha_creacion__date__lte=date_before)
        if vendedor_query:
            base_queryset = base_queryset.filter(vendedor__nombre__icontains=vendedor_query)

        # Perform calculations on the final, filtered queryset
        total_operaciones_periodo = base_queryset.count()
        conteo_por_estado = base_queryset.values('estado').annotate(count=Count('folio')).order_by('estado')
        corte_de_caja = base_queryset.filter(pagado=True).aggregate(total=Sum('costo'))['total'] or 0.00

        # Expired packages logic (Current Month)
        from django.utils import timezone
        now = timezone.now()
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Filter for expired packages in the current month within the base queryset (respecting permissions)
        paquetes_expirados_qs = base_queryset.filter(
            fecha_expiracion__gte=start_of_month.date(),
            fecha_expiracion__lte=now.date(), # Assuming expiration date is effectively "expired" if it's in the past or today
            # You might want to adjust this logic depending on exactly how you define "expired this month"
            # If it means "expiration date falls within this month":
            # fecha_expiracion__year=now.year,
            # fecha_expiracion__month=now.month
        )
        
        # Using the "expiration date falls within this month" logic as per requirement T11 usually implies
        paquetes_expirados_qs = base_queryset.filter(
            fecha_expiracion__year=now.year,
            fecha_expiracion__month=now.month
        )

        paquetes_expirados_data = [
            {
                'folio': op.folio,
                'vendedor_nombre': op.vendedor.nombre if op.vendedor else 'N/A',
                'fecha_expiracion': op.fecha_expiracion,
                'costo': op.costo
            }
            for op in paquetes_expirados_qs
        ]

        data = {
            'total_operaciones_periodo': total_operaciones_periodo,
            'corte_de_caja': corte_de_caja,
            'conteo_por_estado': list(conteo_por_estado),
            'paquetes_expirados': paquetes_expirados_data
        }

        return Response(data)


import csv
from django.http import HttpResponse

class OperacionExportView(generics.ListAPIView):
    """
    Vista para exportar operaciones a CSV.
    Reutiliza los filtros y permisos de la lista.
    """
    serializer_class = OperacionSerializer
    filterset_class = OperacionFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Reutilizamos la lógica de filtrado base
        user = self.request.user
        if user.role == 'ADMIN' or user.is_superuser:
            return Operacion.objects.all()
        elif user.sucursal:
            return Operacion.objects.filter(models.Q(sucursal_origen=user.sucursal) | models.Q(sucursal_destino=user.sucursal))
        return Operacion.objects.none()

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="operaciones.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Folio', 'Vendedor', 'Comprador', 'Sucursal Origen', 
            'Sucursal Destino', 'Estado', 'Costo', 'Pagado', 'Fecha Creación', 'Fecha Expiración'
        ])

        for op in queryset:
            writer.writerow([
                op.folio,
                op.vendedor.nombre if op.vendedor else 'N/A',
                op.comprador,
                op.sucursal_origen.nombre,
                op.sucursal_destino.nombre,
                op.get_estado_display(),
                op.costo,
                'Sí' if op.pagado else 'No',
                op.fecha_creacion.strftime('%Y-%m-%d %H:%M'),
                op.fecha_expiracion
            ])

        return response
