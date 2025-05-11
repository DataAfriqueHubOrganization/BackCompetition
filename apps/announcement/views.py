# views.py
from rest_framework import viewsets, permissions, status
# Import standard DRF permissions
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from .models import Announcement
from .serializers import AnnouncementSerializer

# Remove imports for generics, APIView, BasePermission, SAFE_METHODS if no longer needed elsewhere


###################################################################################
#                                ANNOUNCEMENT                                    #
###################################################################################

class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Announcements.
    - List/Retrieve: Authenticated users.
    - Create/Update/Destroy: Admin users only.
    - The 'user' field is automatically set to the request user upon creation.
    """
    # Optimize DB query by fetching the related user in the same query
    queryset = Announcement.objects.select_related('user').all().order_by('-created_at')
    serializer_class = AnnouncementSerializer

    def get_permissions(self):
        """
        Assign permissions based on action.
        - Admin required for write actions (create, update, destroy).
        - Authenticated required for read actions (list, retrieve).
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only admin users can perform these actions
            permission_classes = [permissions.IsAdminUser]
        else:
            # Any authenticated user can list or retrieve announcements
            # Change to [permissions.AllowAny] if you want anyone to see them
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """
        Override perform_create to automatically set the user field
        to the user making the request.
        """
        # serializer.save() will call the model's save() method
        # We pass the user from the request context here.
        serializer.save(user=self.request.user)

    # Optional: Add Swagger documentation hints
    @swagger_auto_schema(
        operation_description="List all announcements (**Public Access**).",
        responses={200: AnnouncementSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new announcement (Admin only). User is set automatically.",
        responses={201: AnnouncementSerializer, 400: "Invalid Data", 403: "Permission Denied"}
        # request_body is inferred from serializer_class
    )
    def create(self, request, *args, **kwargs):
        # perform_create handles setting the user
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific announcement (**Public Access**).",
        responses={200: AnnouncementSerializer, 404: "Not Found"}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update an announcement (Admin only).",
        responses={200: AnnouncementSerializer, 400: "Invalid Data", 403: "Permission Denied", 404: "Not Found"}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update an announcement (Admin only).",
        responses={200: AnnouncementSerializer, 400: "Invalid Data", 403: "Permission Denied", 404: "Not Found"}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete an announcement (Admin only).",
        responses={204: "No Content", 403: "Permission Denied", 404: "Not Found"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)