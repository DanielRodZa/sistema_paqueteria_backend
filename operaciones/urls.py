from django.urls import path
from .views import OperacionListCreateView, OperacionDetailView, ReportesView

urlpatterns = [
    path('operaciones/', OperacionListCreateView.as_view(), name='lista-crear-operaciones'),
    path('operaciones/<str:folio>/', OperacionDetailView.as_view(), name='detalle-operacion'),
    path('reportes/', ReportesView.as_view(), name='reportes'),
]