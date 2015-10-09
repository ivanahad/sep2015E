from django.shortcuts import render
from django.http import HttpResponseRedirect
from players.models import Pair
from tournament.models import *
from tournament.forms import LaunchTournamentForm
import math

def launch(request):
    if request.method == 'POST':
        form = LaunchTournamentForm(request.POST)
        if form.is_valid():
            tournament = Tournament.objects.get(name=form.cleaned_data['name'])
            #list of players from database
            pairs_key = TournamentParticipant.objects.filter(tournament=tournament)
            pairs = [entry.participant for entry in pairs_key]
            std_size = tournament.pool_size
            nb_pools = math.ceil(len(pairs) / std_size)
            nb_reduced_pools = (nb_pools * std_size) - len(pairs)
            pools = [] #creates a list of new pools.
            for i in range(nb_pools) :
                pools.append(Pool())
                pools[i].size = (std_size-1) if i < nb_reduced_pools else std_size

            pairs = set(pairs)
            for pool in pools :
                pool.tournament = tournament
                pool.save()
                for i in range(pool.size):
                    pp = PoolParticipant()
                    pp.pool = pool
                    pp.participant = pairs.pop()
                    pp.save()
                parts = [pp.participant for pp in \
                        PoolParticipant.objects.filter(pool=pool)]
                for i in range(pool.size):
                    for j in range(i+1, pool.size):
                        match = Match()
                        match.team1 = parts[i]
                        match.team2 = parts[j]
                        match.save()
            return HttpResponseRedirect('/')
    else:
        form = LaunchTournamentForm()
        return render(request, 'tournament/launch.html', locals())
