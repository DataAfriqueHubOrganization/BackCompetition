from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.permissions import IsAuthenticated, AllowAny
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

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff
    
class IsOwner(BasePermission):
    """
    Autorise seulement l’auteur d’un commentaire à le modifier ou supprimer.
    """
    def has_object_permission(self, request, view, obj):
        # Lecture seule (GET, HEAD, OPTIONS) autorisée pour tous
        if request.method in SAFE_METHODS:
            return True
        # Sinon, seul l'auteur peut modifier ou supprimer
        return obj.users == request.user
class IsOwnerOrAdmin(BasePermission):
    """
    Permet à l'auteur ou à l'admin de modifier/supprimer un commentaire.
    Les autres peuvent uniquement lire.
    """
    def has_object_permission(self, request, view, obj):
        # Permet à tous de lire
        if request.method in SAFE_METHODS:
            return True
        # Seul l'auteur ou l'admin peut modifier/supprimer
        return obj.users == request.user or request.user.is_staff or request.user.is_superuser
