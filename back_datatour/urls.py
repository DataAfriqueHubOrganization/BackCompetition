from django.urls import path

from back_datatour.views import UserRegister

from django.urls import path
from .views import (
    CommentListCreateAPIView,
    CommentRetrieveUpdateDestroyAPIView,
    AnnouncementListCreateAPIView,
    AnnouncementRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("register/", UserRegister.as_view(), name='users_register'),

    # Endpoints pour Comment
    path('comments/', CommentListCreateAPIView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment-detail'),
    
    # Endpoints pour Announcement
    path('announcements/', AnnouncementListCreateAPIView.as_view(), name='announcement-list'),
    path('announcements/<int:pk>/', AnnouncementRetrieveUpdateDestroyAPIView.as_view(), name='announcement-detail'),
]

