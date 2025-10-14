from django_filters import rest_framework as filters
from .models import Operacion

class OperacionFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name='fecha_creacion', lookup_expr='date__gte')
    end_date = filters.DateFilter(field_name='fecha_creacion', lookup_expr='date__lte')

    class Meta:
        model = Operacion
        fields = {
            'vendedor__nombre': ['icontains'],
            'comprador': ['icontains'],
            'estado': ['exact'],
        }