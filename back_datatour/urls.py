# from django.urls import path, include
# from .views import *
# from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework.routers import DefaultRouter

# # Initialiser le router
# router = DefaultRouter()
# router.register(r'countries', CountryViewSet)
# router.register(r'competitions', CompetitionViewSet)
# router.register(r'phases', CompetitionPhaseViewSet)
# router.register(r'datasets', DatasetViewSet, basename='dataset')
# router.register(r'challenges', ChallengeViewSet, basename='challenge')
# router.register(r'leaderboards', LeaderboardViewSet)
# router.register(r'submissions', SubmissionViewSet, basename='submission')



urlpatterns = [

#     path('auth/register/', RegisterView.as_view(), name='register'),
#     path('auth/verify-email/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
    
#     path('login/', LoginView.as_view(), name='login'),  # API de login
#     path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # API de refresh de token
#     path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
#     path('reset-password/<uidb64>/<token>/', ResetPasswordView.as_view(), name='reset_password'),
#     path('change-password/', ChangePasswordView.as_view(), name='change_password'),
#     path('deactivate-account/', DeactivateAccountView.as_view(), name='deactivate-account'),

#     path("users", ListUser.as_view(), name='list_users'),
#     path("users/<uuid:pk>", UserDetail.as_view(), name='user_detail'),
    
#     path("partners", ListOrCreatePartner.as_view(), name='list_or_create_partners'),
#     path("partners/<uuid:pk>", PartnerDetail.as_view(), name='partner_detail'),
#     path("teams", ListOrCreateTeam.as_view(), name="list_or_create_teams"),
#     path("teams/<uuid:pk>", TeamDetail.as_view(), name="team_detail"),
    
#     # Endpoints pour Comment
#     path('comments/', CommentListCreateAPIView.as_view(), name='comment-list'),
#     path('comments/<uuid:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment-detail'),
    
#     # Endpoints pour Announcement
#     path('announcements/', AnnouncementListCreateAPIView.as_view(), name='announcement-list'),
#     path('announcements/<uuid:pk>/', AnnouncementRetrieveUpdateDestroyAPIView.as_view(), name='announcement-detail'),
    
#     ## challenge

#     path('challenges/', ChallengeListCreateView.as_view(), name='challenge-list-create'),
#     path('challenges/<uuid:pk>/', ChallengeDetailView.as_view(), name='challenge-detail'),
    
#     path('', include(router.urls)),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

