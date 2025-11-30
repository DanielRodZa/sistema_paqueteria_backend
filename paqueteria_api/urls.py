from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/operaciones/', include('operaciones.urls')),
    path('api/vendedores/', include('vendedores.urls')),
    path('api/sucursales/', include('sucursales.urls')),
    path('api/users/', include('users.urls')),
    path('api/configuracion/', include('configuracion.urls')),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]