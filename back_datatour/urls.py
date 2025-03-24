from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    
    path('login/', LoginView.as_view(), name='login'),  # API de login
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # API de refresh de token
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset_password'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('deactivate-account/', DeactivateAccountView.as_view(), name='deactivate-account'),
    
    path("partners", ListOrCreatePartner.as_view(), name='list_or_create_partners'),
    path("partners/<int:pk>", PartnerDetail.as_view(), name='partner_detail'),
    path("teams", ListOrCreateTeam.as_view(), name="list_or_create_teams"),
    path("teams/<int:pk>", TeamDetail.as_view(), name="team_detail"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
