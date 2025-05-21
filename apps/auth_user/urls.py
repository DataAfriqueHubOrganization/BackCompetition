from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'admins', AdminUserViewSet, basename='admin-user')
router.register(r'countries', CountryViewSet)


urlpatterns = [
    path('', include(router.urls)),
    
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),  # API de login
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # API de refresh de token
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('deactivate-account/', DeactivateAccountView.as_view(), name='deactivate-account'),
    path("users", ListUser.as_view(), name='list_users'),
    path("users/<uuid:pk>", UserDetail.as_view(), name='user_detail'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





    

