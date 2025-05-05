# apps/comment/filters.py
import django_filters
from .models import Comment

class CommentFilter(django_filters.FilterSet):
    """
    FilterSet for the Comment model.
    Allows filtering by user and competition_phase using their IDs.
    """
    # You can define specific lookup types if needed, but the default
    # for ForeignKey is exact match on the primary key, which is perfect here.
    # Example: user = django_filters.UUIDFilter(field_name='user_id', lookup_expr='exact')

    class Meta:
        model = Comment
        # Define the fields available for filtering
        fields = {
            'user': ['exact'],  # Allows ?user=<user_uuid>
            'competition_phase': ['exact'], # Allows ?competition_phase=<phase_uuid>
                   }
       