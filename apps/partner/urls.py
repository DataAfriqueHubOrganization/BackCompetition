from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    
    path("partners", ListOrCreatePartner.as_view(), name='list_or_create_partners'),
    path("partners/<uuid:pk>", PartnerDetail.as_view(), name='partner_detail'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

