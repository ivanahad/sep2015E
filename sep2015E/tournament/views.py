from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from tournament.models import Tournament, TournamentParticipant, \
        Pool, PoolParticipant, PoolMatch
from tournament.forms import OpenTournamentChoiceForm, CreateTournamentForm

def all(request):
    if request.method == 'POST':
        new_trn = CreateTournamentForm(request.POST)
        if new_trn.is_valid():
            tournament = Tournament( \
                    name = new_trn.cleaned_data['name'], \
                    category = new_trn.cleaned_data['category'], \
                    pool_size = new_trn.cleaned_data['pool_size'], \
                    season = settings.CURRENT_SEASON, \
                )
            tournament.save()

        return HttpResponseRedirect('/tournament/all')
        
    else:
        tournaments = Tournament.objects\
                .filter(season=settings.CURRENT_SEASON)
        tournaments = [(tournament, \
                TournamentParticipant.objects\
                .filter(tournament=tournament).count(), \
                "open" if tournament.is_open else "closed" \
                ) for tournament in tournaments]
        new_trn = CreateTournamentForm()

        return render(request, 'tournament/all.html', { \
                'tournaments': tournaments, \
                'new_tournament': new_trn, \
                })

def tournament(request, id_):
    id_ = int(id_)
    try:
        tournament = Tournament.objects.get(pk=id_)
        if request.method == 'POST':
            if 'close_tournament' in request.POST:
                tournament.close_registrations()

            return HttpResponseRedirect('/tournament/all')
            #return HttpResponseRedirect( \
            #        '/tournament/detail?id=' + tournament.pk)

        else:
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
                    'pools': pools, \
                    })

    except Tournament.DoesNotExist:
        return HttpResponseRedirect('/tournament/all')

def pool(request, id_tournament, id_pool):
    tournament = Tournament.objects.get(pk=id_tournament)
    pool = Pool.objects.filter(tournament=tournament, number=id_pool)
    pool = (pool, PoolParticipant.objects.filter(pool=pool))
    pool_matches = PoolMatch.objects.filter(pool=pool)

    return render(request, 'tournament/pool.html', { \
            'trn': tournament, \
            'pool': pool, \
            'pool_matches': pool_matches \
            })
