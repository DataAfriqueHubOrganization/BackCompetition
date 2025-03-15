from django.contrib import admin

from back_datatour.models import Users, Team, Competition, CompetitionPhase,Partner

# Register your models here.
admin.site.register(Users)
admin.site.register(Team)
admin.site.register(Competition)
admin.site.register(CompetitionPhase)
admin.site.register(Partner)