from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    Permite el acceso solo a usuarios con el rol de Administrador.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'ADMIN'


class IsAdminOrManagerUser(BasePermission):
    """
    Permite el acceso a usuarios con rol de Administrador o Manager.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role in ['ADMIN', 'MANAGER']


class CanMarkAsPaidPermission(BasePermission):
    """
    Permiso que permite a cualquier usuario autenticado marcar una operación como pagada,
    pero solo si es el único campo que se está modificando.
    """

    def has_object_permission(self, request, view, obj):
        if request.method not in ['PUT', 'PATCH']:
            return True

        restricted_fields = ['vendedor', 'comprador', 'tamano_paquete', 'sucursal_origen', 'sucursal_destino', 'costo']

        for field in restricted_fields:
            if field in request.data:
                return False

        return True


class IsManagerUser(BasePermission):
    """
    Permite el acceso solo a usuarios con el rol de Manager.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'MANAGER'
