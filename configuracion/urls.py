from django.urls import path
from .views import ConfiguracionRetrieveUpdateView

urlpatterns = [
    path('', ConfiguracionRetrieveUpdateView.as_view(), name='configuracion-detail'),
]
