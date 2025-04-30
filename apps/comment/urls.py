from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    
#     Endpoints pour Comment
    path('', CommentListCreateAPIView.as_view(), name='comment-list'),
    path('<uuid:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment-detail'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

