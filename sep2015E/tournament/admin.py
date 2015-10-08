from django.contrib import admin

from .models import Tournament, TournamentParticipant, Pool, PoolParticipant, Match, PoolMatch, TournamentNode

admin.site.register(Tournament)
admin.site.register(TournamentParticipant)
admin.site.register(Pool)
admin.site.register(PoolParticipant)
admin.site.register(Match)
admin.site.register(PoolMatch)
admin.site.register(TournamentNode)