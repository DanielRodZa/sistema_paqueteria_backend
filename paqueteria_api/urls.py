from django.contrib import admin
from django.urls import path, include
from users.views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('operaciones.urls')),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/vendedores/', include('vendedores.urls')),
    path('api/sucursales/', include('sucursales.urls')),
    path('api/users/', include('users.urls')),
]