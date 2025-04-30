from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

# # Initialiser le router
router = DefaultRouter()
router.register(r'datasets', DatasetViewSet, basename='dataset')




urlpatterns = [
 
    path('', include(router.urls)),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

