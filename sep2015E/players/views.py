from django.shortcuts import render
from django.http import HttpResponseRedirect
from players.forms import RegisterForm
from players.models import User, Pair
from tournament.forms import OpenTournamentChoiceForm
from tournament.models import TournamentParticipant

def register(request):
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form1 = RegisterForm(request.POST, prefix="form1")
        form2 = RegisterForm(request.POST, prefix="form2")
        tourn = OpenTournamentChoiceForm(request.POST)

        if form1.is_valid() and form2.is_valid() and tourn.is_valid():

            new_user1 = User(firstname = form1.cleaned_data['firstname'], \
                    lastname = form1.cleaned_data['lastname'], \
                    address = form1.cleaned_data['address'], \
                    city = form1.cleaned_data['city'], \
                    country = form1.cleaned_data['country'], \
                    zipcode = form1.cleaned_data['zipcode'], \
                    email = form1.cleaned_data['email'], \
                    phone = form1.cleaned_data['phone'], \
                    level = form1.cleaned_data['level'], \
                    bbq = form1.cleaned_data['bbq'], \
                    comment = form1.cleaned_data['comment'])
            new_user1.save()

            new_user2 = User(firstname = form2.cleaned_data['firstname'], \
                    lastname = form2.cleaned_data['lastname'], \
                    address = form2.cleaned_data['address'], \
                    city = form2.cleaned_data['city'], \
                    country = form2.cleaned_data['country'], \
                    zipcode = form2.cleaned_data['zipcode'], \
                    email = form2.cleaned_data['email'], \
                    phone = form2.cleaned_data['phone'], \
                    level = form2.cleaned_data['level'], \
                    bbq = form2.cleaned_data['bbq'], \
                    comment = form2.cleaned_data['comment'])
            new_user2.save()

            new_pair = Pair(player1 = new_user1, player2 = new_user2, average = 0)
            new_pair.save()

            tournament = tourn.cleaned_data['tournament']
            tp = TournamentParticipant()
            tp.participant = new_pair
            tp.tournament = tournament
            tp.save()

            return render(request, 'players/payement.html')

    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        form1 = RegisterForm(prefix="form1")
        form2 = RegisterForm(prefix="form2")  # Nous créons un formulaire vide
        tourn = OpenTournamentChoiceForm()

        return render(request, 'players/register.html', {
            'form1': form1,
            'form2': form2,
            'tourn': tourn
        })

def payement(request):
    return render(request, 'players/payement.html')
