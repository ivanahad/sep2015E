from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from tournament.models import Tournament, TournamentParticipant, \
        Pool, PoolParticipant, PoolMatch, Match
from tournament.forms import OpenTournamentChoiceForm, CreateTournamentForm, \
        MatchEditForm

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
    if request.method == 'POST':
        form = MatchEditForm(request.POST)
        if form.is_valid():
            score1 = form.cleaned_data['score1']
            score2 = form.cleaned_data['score2']
            court = form.cleaned_data['court']
            team1 = form.clean_team1()
            team2 = form.clean_team2()
            match = Match.objects.filter(team1=team1, team2=team2)
            match = match.get()
            match.team1 = team1
            match.team2 = team2
            match.score1 = score1
            match.score2 = score2
            match.court = court
            match.save()
    else:
        id_match = 0
        form = MatchEditForm()
    return render(request, 'tournament/pool.html', { \
            'trn': tournament, \
            'pool': pool, \
            'pool_matches': pool_matches, \
            'form' : form \
            })
