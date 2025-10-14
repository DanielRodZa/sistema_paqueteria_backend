from django.urls import path
from .views import VendedorListCreateView, VendedorDetailView

urlpatterns = [
    path('', VendedorListCreateView.as_view(), name='lista-crear-vendedores'),
    path('<str:pk>/', VendedorDetailView.as_view(), name='detalle-vendedor'),
]