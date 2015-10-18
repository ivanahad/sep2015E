from django.shortcuts import render
from tournament.models import Tournament, TournamentParticipant
from django.conf import settings

def all(request):
    tournaments = Tournament.objects.filter(season=settings.CURRENT_SEASON)
    tournaments = [(tournament, \
            TournamentParticipant.objects\
            .filter(tournament=tournament).count(), \
            "open" if tournament.is_open else "closed" \
            )
            for tournament in tournaments]

    return render(request, 'tournament/all.html', { \
            'tournaments': tournaments\
            })
