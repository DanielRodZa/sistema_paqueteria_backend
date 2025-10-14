from django.urls import path
from .views import SucursalListCreateView, SucursalDetailView


urlpatterns = [
    path('', SucursalListCreateView.as_view(), name='lista-crear-sucursales'),
    path('<str:pk>/', SucursalDetailView.as_view(), name='detalle-sucursal'),
]