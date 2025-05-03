# views.py
from rest_framework import viewsets, permissions, status
# Make sure all needed permissions are imported
from rest_framework.permissions import IsAuthenticated, BasePermission, IsAuthenticatedOrReadOnly, SAFE_METHODS
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi 
from .models import Comment, CompetitionPhase # Import models
from .serializers import CommentSerializer, CommentUpdateSerializer  # Import serializer

from django_filters.rest_framework import DjangoFilterBackend

from .filters import CommentFilter
class IsOwnerOrAdmin(BasePermission):
    """
    Autorise la modification ou la suppression seulement si l'utilisateur est
    le propriétaire (champ 'users') ou un administrateur.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.is_staff or request.user.is_superuser

class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Comments on Competition Phases.
    - List/Retrieve: Anyone. Supports filtering.
    - Create: Authenticated users (requires 'competition_phase' ID and 'content').
    - Update/Destroy: Comment Owner or Admin only (updates only 'content').
    """
    queryset = Comment.objects.select_related('user', 'competition_phase').all().order_by('-created_at')
    # serializer_class = CommentSerializer # <- Supprimer la définition par défaut ici

    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentFilter

    def get_serializer_class(self):
        """
        Retourne la classe de serializer appropriée en fonction de l'action.
        """
        if self.action in ['update', 'partial_update']:
            # Utilise le serializer restreint pour les mises à jour
            return CommentUpdateSerializer
        # Pour toutes les autres actions (list, retrieve, create), utilise le serializer complet
        return CommentSerializer

    def get_permissions(self):
        """ Assigns permissions based on action. """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """ Set the user of the comment to the logged-in user. """
        # Le serializer ici sera CommentSerializer (grâce à get_serializer_class)
        # Il contient competition_phase et content dans validated_data
        serializer.save(user=self.request.user)

    # --- Swagger documentation (ajustée pour request_body de update/patch) ---
    @swagger_auto_schema(
        operation_description="List all comments (Public Access)...",
        manual_parameters=[...], # Garder les paramètres de filtre
        responses={200: CommentSerializer(many=True)} # Réponse utilise CommentSerializer
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new comment...",
        request_body=CommentSerializer, # Input utilise CommentSerializer
        responses={201: CommentSerializer} # Réponse utilise CommentSerializer
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific comment...",
        responses={200: CommentSerializer} # Réponse utilise CommentSerializer
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a comment (Owner or Admin only). Only 'content' can be modified.",
        # request_body est maintenant inféré depuis get_serializer_class comme étant CommentUpdateSerializer
        responses={200: CommentSerializer} # La réponse affiche toujours le commentaire complet
    )
    def update(self, request, *args, **kwargs):
        # super().update() utilisera CommentUpdateSerializer pour valider l'input
        # mais retournera le résultat sérializé par CommentSerializer (comportement par défaut)
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a comment (Owner or Admin only). Only 'content' can be modified.",
         # request_body est inféré comme CommentUpdateSerializer
        responses={200: CommentSerializer} # La réponse affiche toujours le commentaire complet
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a comment (Owner or Admin only).",
        responses={204: 'No content', 401/403: "Permission Denied", 404: "Not Found"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)