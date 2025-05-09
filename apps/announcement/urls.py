from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
#     # Endpoints pour Announcement
    path('', AnnouncementListCreateAPIView.as_view(), name='announcement-list'),
    path('<uuid:pk>/', AnnouncementRetrieveUpdateDestroyAPIView.as_view(), name='announcement-detail'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

