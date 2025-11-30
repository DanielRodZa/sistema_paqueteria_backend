from django.urls import path
from .views import OperacionListCreateView, OperacionDetailView, ReportesView

urlpatterns = [
    path('reportes/', ReportesView.as_view(), name='reportes'),
    path('', OperacionListCreateView.as_view(), name='lista-crear-operaciones'),
    path('<str:folio>/', OperacionDetailView.as_view(), name='detalle-operacion'),
]