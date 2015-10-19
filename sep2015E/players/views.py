from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from players.forms import PlayerForm, RegistrationForm
from players.models import User, Pair, UserRegistration
from tournament.forms import OpenTournamentChoiceForm
from tournament.models import TournamentParticipant

def register(request):
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        usr1 = PlayerForm(request.POST, prefix="usr1")
        reg1 = RegistrationForm(request.POST, prefix="reg1")
        usr2 = PlayerForm(request.POST, prefix="usr2")
        reg2 = RegistrationForm(request.POST, prefix="reg2")
        trn = OpenTournamentChoiceForm(request.POST)

        if usr1.is_valid() and usr2.is_valid() \
                and reg1.is_valid() and reg2.is_valid() \
                and trn.is_valid():

            new_user1 = User( \
                    firstname = usr1.cleaned_data['firstname'], \
                    lastname = usr1.cleaned_data['lastname'], \
                    address = usr1.cleaned_data['address'], \
                    city = usr1.cleaned_data['city'], \
                    country = usr1.cleaned_data['country'], \
                    zipcode = usr1.cleaned_data['zipcode'], \
                    email = usr1.cleaned_data['email'], \
                    phone = usr1.cleaned_data['phone'])
            new_user1.save()

            registration1 = UserRegistration( \
                    user = new_user1, \
                    season = settings.CURRENT_SEASON, \
                    payment_method = reg1.cleaned_data['payment_method'], \
                    bbq = reg1.cleaned_data['bbq'], \
                    activities = reg1.cleaned_data['activities'], \
                    comment = reg1.cleaned_data['comment'], \
                    level = reg1.cleaned_data['level'])
            registration1.save()


            new_user2 = User( \
                    firstname = usr2.cleaned_data['firstname'], \
                    lastname = usr2.cleaned_data['lastname'], \
                    address = usr2.cleaned_data['address'], \
                    city = usr2.cleaned_data['city'], \
                    country = usr2.cleaned_data['country'], \
                    zipcode = usr2.cleaned_data['zipcode'], \
                    email = usr2.cleaned_data['email'], \
                    phone = usr2.cleaned_data['phone'])
            new_user2.save()

            registration2 = UserRegistration( \
                    user = new_user2, \
                    season = settings.CURRENT_SEASON, \
                    payment_method = reg2.cleaned_data['payment_method'], \
                    bbq = reg2.cleaned_data['bbq'], \
                    activities = reg2.cleaned_data['activities'], \
                    comment = reg2.cleaned_data['comment'], \
                    level = reg2.cleaned_data['level'])
            registration2.save()


            new_pair = Pair( \
                    player1 = new_user1, \
                    player2 = new_user2, \
                    average = 0, \
                    season = settings.CURRENT_SEASON)
            new_pair.save()

            tp = TournamentParticipant( \
                    participant = new_pair,
                    tournament = trn.cleaned_data['tournament'])
            tp.save()

            return render(request, 'players/registration_success.html')

        else:
            return render(request, 'players/registration_failure.html')

    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        usr1 = PlayerForm(prefix="usr1")
        reg1 = RegistrationForm(prefix="reg1")
        usr2 = PlayerForm(prefix="usr2")
        reg2 = RegistrationForm(prefix="reg2")
        trn = OpenTournamentChoiceForm()

        return render(request, 'players/register.html', {
            "usr1": usr1,
            "reg1": reg1,
            "usr2": usr2,
            "reg2": reg2,
            "trn": trn
        })
