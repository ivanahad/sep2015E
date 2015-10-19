from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from tournament.models import Tournament, TournamentParticipant, \
        Pool, PoolParticipant

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

def tournament(request):
    if request.method == 'POST':
        # not supported
        return HttpResponseRedirect('/tournament/all')
    else:
        id_ = int(request.GET.get('id', ''))
        try:
            tournament = Tournament.objects.get(pk=id_)
            parts = [p.participant for p in \
                    TournamentParticipant.objects\
                    .filter(tournament=tournament)]
            pools = Pool.objects.filter(tournament=tournament)
            pools = [(p, PoolParticipant.objects.filter(pool=p)) \
                    for p in pools]
            return render(request, 'tournament/detail.html', { \
                    'trn': tournament, \
                    'parts': parts, \
                    'nbr': len(parts), \
                    'pools': pools \
                    })

        except Tournament.DoesNotExist:
            return HttpResponseRedirect('/tournament/all')
