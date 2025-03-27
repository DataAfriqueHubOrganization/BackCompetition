from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Users)
admin.site.register(Team)
admin.site.register(Competition)
admin.site.register(CompetitionPhase)
admin.site.register(Country)

