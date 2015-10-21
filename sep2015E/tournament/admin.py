from django.contrib import admin

from .models import *

def close_action(modeladmin, request, queryset):
    for tournament in queryset:
        tournament.close_registrations()
close_action.short_description = "Close tournament"

def open_action(modeladmin, request, queryset):
    for tournament in queryset:
        for p in Pool.objects.filter(tournament=tournament):
            for pm in PoolMatch.objects.filter(pool=p):
                pm.match.delete()
            p.delete()
        tournament.is_open = True
        tournament.save()
open_action.short_description = "Open tournament"

class MyAdmin(admin.ModelAdmin):
    list_display=('name', 'category', 'is_open')
    actions = [close_action, open_action]

admin.site.register(Tournament, MyAdmin)
admin.site.register(TournamentParticipant)
admin.site.register(SoloParticipant)
admin.site.register(Pool)
admin.site.register(PoolParticipant)
admin.site.register(Match)
admin.site.register(PoolMatch)
admin.site.register(TournamentNode)
