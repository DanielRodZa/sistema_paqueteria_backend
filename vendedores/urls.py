from django.urls import path
from .views import VendedorListCreateView, VendedorDetailView, VendedorExportView

urlpatterns = [
    path('', VendedorListCreateView.as_view(), name='lista-crear-vendedores'),
    path('export/', VendedorExportView.as_view(), name='export-vendedores'),
    path('<str:pk>/', VendedorDetailView.as_view(), name='detalle-vendedor'),
]