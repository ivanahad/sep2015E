from math import ceil
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from tournament.models import *
from players.models import *
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
                    mixte = new_trn.cleaned_data['mixte'], \
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

def allUser(request):
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

    return render(request, 'tournament/allUser.html', { \
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

def tournamentStaff(request, id_):
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
            return render(request, 'tournament/detailStaff.html', { \
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
    """ Page for visualing a particular pool """
    tournament = Tournament.objects.get(pk=id_tournament)
    pool = Pool.objects.filter(tournament=tournament, number=id_pool).get()
    pool_matches = PoolMatch.objects.filter(pool=pool)
    participants = PoolParticipant.objects.filter(pool=pool)
    matches=[]  #List of matches for the pool, the format is the following:
                #[ [pair, [pair_matches]]
                #  [pair, [pair_matches]],... ]
    winner = None
    pool_victories = 0
    i = 0
    for participant in participants:
        partcipant_matches=[]
        j=0
        boolean = False
        number_victory = 0
        for pool_match  in pool_matches:
            if i == j and boolean == False: #leave a blank because pair i can't affront pair i (necessary for the table representation)
                partcipant_matches.append("blank")
                boolean = True
            if pool_match.match.team1==participant.participant or pool_match.match.team2==participant.participant:
                partcipant_matches.append(pool_match.match)
                number_victory += winned(participant.participant, pool_match.match)
                pool_victories += winned(participant.participant, pool_match.match)
                j+=1
        if boolean==False:
            partcipant_matches.append("blank")
        i+=1
        matches.append([participant.participant,partcipant_matches, number_victory])
        if(len(pool_matches) == pool_victories):
            winner = get_winner(matches)


    if request.method == 'POST':
        form = MatchEditForm(request.POST)
        if form.is_valid(): #Form to edit infos of a match
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
            'matches': matches, \
            'form' : form, \
            'winner' : winner\
            })

def get_winner(matches):
    winner = None
    for match in matches:
        if(winner == None):
            winner = match
        else:
            if(match[2] > winner[2]):
                winner = match
    return winner

def winned(pair, match):
    if match.score1 == None or match.score2 == None:
        return 0
    elif pair == match.team1:
        return 1 if match.score1 > match.score2 else 0
    else:
        return 1 if match.score2 > match.score1 else 0

def modify_pools(request, id_tournament, id_page, id_pool):
    """ Page for modifying a pool. The page is divided in two parts,
        one for the list of players not assigned on a tournament
        and the other for the pool."""
    tournament = Tournament.objects.get(pk=id_tournament)

    number_pools=Pool.objects.filter(tournament=tournament).count()
    pool = Pool.objects.filter(tournament=tournament, number=id_pool)
    pool = (pool.get(), PoolParticipant.objects.filter(pool=pool))

    pairs_per_page = 10   #Number of players displayed by page

    all_pools = Pool.objects.filter(tournament=tournament)
    pool_pairs = PoolParticipant.objects.filter(pool=all_pools).values('participant')

    number_pairs = TournamentParticipant.objects.filter(tournament=tournament).exclude(participant=pool_pairs).count()
    number_pages = ceil(number_pairs/pairs_per_page) #Number of pages for the navbar


    extremity1 = 0+(int(id_page)-1)*pairs_per_page    #Range
    extremity2 = (int(id_page)*pairs_per_page)-1
    pairs = TournamentParticipant.objects.filter(tournament=tournament).exclude(participant=pool_pairs)[extremity1:extremity2]

    return render(request, 'tournament/modify_pool.html', { \
        'trn':tournament,
        'pool':pool,
        'pairs':pairs,
        'page_id':int(id_page),
        'number_pages':number_pages,
        'n_pages':range(1, number_pages+1),
        'prev_page':int(id_page)-1,
        'next_page':int(id_page)+1,
        'number_pools':number_pools,
        'n_pools':range(0, number_pools),
        'prev_pool':int(id_pool)-1,
        'next_pool':int(id_pool)+1,
    })

def add_player_to_pool(request, id_tournament, id_page, id_pool, id_pair):
    """ Add a player to a pool."""
    tournament = Tournament.objects.get(pk=id_tournament)
    pool = Pool.objects.filter(tournament=tournament, number=id_pool).get()
    pair = Pair.objects.get(pk=id_pair)
    if not PoolParticipant.objects.filter(pool=pool).count() >= tournament.pool_size: #Check the pool_size limit
        pool_participant = PoolParticipant(pool=pool, participant=pair)
        pool_participant.save()
        for participant in PoolParticipant.objects.filter(pool=pool).exclude(participant=pair):
            match = Match(team1=participant.participant, team2=pair)
            match.save()
            pool_match = PoolMatch(pool=pool, match=match)
            pool_match.save()
    return redirect('tournament.views.modify_pools', id_tournament=id_tournament,
                    id_page=id_page, id_pool=id_pool)


def remove_player_from_pool(request, id_tournament, id_page, id_pool, id_pair):
    """ Remove a player from a pool."""
    tournament = Tournament.objects.get(pk=id_tournament)
    pool = Pool.objects.filter(tournament=tournament, number=id_pool).get()
    pair = PoolParticipant.objects.get(pk=id_pair).participant
    pool_participant = PoolParticipant.objects.filter(pool=pool, participant=pair).get()
    #Delete all matches off the pair
    matches1 = Match.objects.filter(team1=pair)
    matches2 = Match.objects.filter(team2=pair)
    for match in matches1:
        pool_match=PoolMatch.objects.filter(pool=pool,match=match).delete()
    for match in matches2:
        pool_match=PoolMatch.objects.filter(pool=pool,match=match).delete()
    matches1.delete()
    matches2.delete()
    pool_participant.delete()
    return redirect('tournament.views.modify_pools', id_tournament=id_tournament,
                    id_page=id_page, id_pool=id_pool)

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
            if score1 != None:
                match.score1 = score1
            if score2 != None:
                match.score2 = score2
            match.court = court
            match.save()
    return redirect('tournament.views.pool', id_tournament=id_tournament,id_pool=id_pool)
