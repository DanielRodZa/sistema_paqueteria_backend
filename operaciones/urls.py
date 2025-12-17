from django.urls import path
from .views import OperacionListCreateView, OperacionDetailView, ReportesView, OperacionExportView

urlpatterns = [
    path('reportes/', ReportesView.as_view(), name='reportes'),
    path('export/', OperacionExportView.as_view(), name='exportar-operaciones'),
    path('', OperacionListCreateView.as_view(), name='lista-crear-operaciones'),
    path('<str:folio>/', OperacionDetailView.as_view(), name='detalle-operacion'),
]