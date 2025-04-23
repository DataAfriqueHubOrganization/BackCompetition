from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Autorise tout le monde à lire (GET), mais seules les personnes admin peuvent écrire.
    """

    def has_permission(self, request, view):
        # Si c'est une lecture (GET, HEAD, OPTIONS), on autorise tout le monde
        if request.method in permissions.SAFE_METHODS:
            return True
        # Sinon (POST, PUT, DELETE...), on vérifie si l'utilisateur est admin
        return request.user and request.user.is_staff
