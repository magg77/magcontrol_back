# permissions.py, views_mixins.py, (vistas, permisos, etc.)

from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    """
    Permite solo lectura para usuarios anónimos, escritura solo para admins.
    """
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user and request.user.is_staff