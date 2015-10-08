from django.contrib import admin

from .models import Tournament, TournamentParticipant, Pool, PoolParticipant, Match, PoolMatch, TournamentNode

def close_action(modeladmin, request, queryset):
    queryset.update(is_open=False)
close_action.short_description = "Close tournament"

def open_action(modeladmin, request, queryset):
    queryset.update(is_open=True)
open_action.short_description = "Open tournament"

class MyAdmin(admin.ModelAdmin):
    list_display=('name', 'is_open')
    actions = [close_action, open_action]

admin.site.register(Tournament, MyAdmin)
admin.site.register(TournamentParticipant)
admin.site.register(Pool)
admin.site.register(PoolParticipant)
admin.site.register(Match)
admin.site.register(PoolMatch)
admin.site.register(TournamentNode)