from django.urls import path

from back_datatour.views import UserRegister, ListOrCreatePartner, PartnerDetail, ListOrCreateTeam, TeamDetail

urlpatterns = [
    path("register", UserRegister.as_view(), name='users_register'),
    path("partners", ListOrCreatePartner.as_view(), name='list_or_create_partners'),
    path("partners/<int:pk>", PartnerDetail.as_view(), name='partner_detail'),
    path("teams", ListOrCreateTeam.as_view(), name="list_or_create_teams"),
    path("teams/<int:pk>", TeamDetail.as_view(), name="team_detail"),
]
