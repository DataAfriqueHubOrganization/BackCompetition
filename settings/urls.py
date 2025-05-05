from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="Documentation de l'API pour le backend en DRF",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("/", include('back_datatour.urls')),
    path("auth/", include('apps.auth_user.urls')),
    path("announcement/", include('apps.announcement.urls')),
    path("dataset/", include('apps.dataset.urls')),
    path("partner/", include('apps.partner.urls')),
    path("submission/", include('apps.submission.urls')),
    path("competition/", include('apps.competition.urls')),
    path("comment/", include('apps.comment.urls')),
    path("team/", include('apps.team.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ]
