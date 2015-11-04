from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from tournament.models import *
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
        tournaments = [{ \
                "tournament": tournament, \
                "pair_count": TournamentParticipant.objects\
                        .filter(tournament=tournament).count(), \
                "solo_count": SoloParticipant.objects\
                        .filter(tournament=tournament).count(), \
                "status": "open" if tournament.is_open else "closed" \
                } for tournament in tournaments]
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
            solos = [entry.player for entry in \
                    SoloParticipant.objects\
                    .filter(tournament=tournament)]
            pools = Pool.objects.filter(tournament=tournament)
            pools = [(p, PoolParticipant.objects.filter(pool=p)) \
                    for p in pools]
            return render(request, 'tournament/detail.html', { \
                    'trn': tournament, \
                    'parts': parts, \
                    'nbr_p': len(parts), \
                    'solos': solos, \
                    'nbr_s': len(solos), \
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
        form = MatchEditForm()
    return render(request, 'tournament/pool.html', { \
            'trn': tournament, \
            'pool': pool, \
            'pool_matches': pool_matches, \
            'form' : form \
            })

def save_match_changes(request, id_tournament, id_pool, id_match):
    """Save the changes when editing the match and redirect to the pool where the match has been edited."""
    if request.method == 'POST':
        form = MatchEditForm(request.POST)
        if form.is_valid():
            score1 = form.cleaned_data['score1']
            score2 = form.cleaned_data['score2']
            court = form.cleaned_data['court']
            match = Match.objects.filter(id=id_match)
            match = match.get()
            match.score1 = score1
            match.score2 = score2
            match.court = court
            match.save()
    return redirect('tournament.views.pool', id_tournament=id_tournament,id_pool=id_pool)
