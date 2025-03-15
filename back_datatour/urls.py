from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
from .views import (
    UserViewSet, CountryViewSet, TeamViewSet, PartnerViewSet,
    CompetitionViewSet, CompetitionPhaseViewSet, LeaderboardViewSet,
    DatasetViewSet, ChallengeViewSet, SubmissionViewSet,
    CommentViewSet, AnnouncementViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'partners', PartnerViewSet)
router.register(r'competitions', CompetitionViewSet)
router.register(r'competition-phases', CompetitionPhaseViewSet)
router.register(r'leaderboards', LeaderboardViewSet)
router.register(r'datasets', DatasetViewSet)
router.register(r'challenges', ChallengeViewSet)
router.register(r'submissions', SubmissionViewSet, basename='submission')
router.register(r'comments', CommentViewSet)
router.register(r'announcements', AnnouncementViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
