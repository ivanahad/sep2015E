from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from players.forms import PlayerForm, RegistrationForm, EmailOldUserForm
from players.models import User, Pair, UserRegistration
from tournament.forms import OpenTournamentChoiceForm
from tournament.models import TournamentParticipant, SoloParticipant, Tournament
from django.core.mail import send_mail

def register(request):
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        usr1 = PlayerForm(request.POST, prefix="usr1")
        reg1 = RegistrationForm(request.POST, prefix="reg1")
        usr2 = PlayerForm(request.POST, prefix="usr2")
        reg2 = RegistrationForm(request.POST, prefix="reg2")
        trn = OpenTournamentChoiceForm(request.POST)
        if 'solo_registration' in request.POST \
                and usr1.is_valid() and reg1.is_valid() \
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

            solo_registration = SoloParticipant( \
                    player = new_user1, \
                    tournament = trn.cleaned_data['tournament'])
            solo_registration.save()

            send_mail('Enregistrement à un tournoi', 'Bonjour '+usr1.cleaned_data['firstname']+' '+usr1.cleaned_data['lastname']+',\n\nAsmae vous confirme que vous avez bien été inscrit au tournoi ' \
                +trn.cleaned_data['tournament'].name+' '+trn.cleaned_data['tournament'].category, 'info@sep2015e.com', [usr1.cleaned_data['email']], fail_silently=False)

            return render(request, 'players/registration_success.html')

        elif usr1.is_valid() and usr2.is_valid() \
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

            Pair.create_pair(new_user1, new_user2)

            send_mail('Enregistrement à un tournoi', 'Bonjour '+usr1.cleaned_data['firstname']+' '+usr1.cleaned_data['lastname']+',\n\nAsmae vous confirme que vous avez bien été inscrit au tournoi ' \
                +trn.cleaned_data['tournament'].name+' '+trn.cleaned_data['tournament'].category+' avec votre partenaire '+usr2.cleaned_data['firstname']+' '+usr2.cleaned_data['lastname'], 'info@sep2015e.com', [usr1.cleaned_data['email']], fail_silently=False)

            send_mail('Enregistrement à un tournoi', 'Bonjour '+usr2.cleaned_data['firstname']+' '+usr2.cleaned_data['lastname']+',\n\nAsmae vous confirme que vous avez bien été inscrit au tournoi ' \
                +trn.cleaned_data['tournament'].name+' '+trn.cleaned_data['tournament'].category+' avec votre partenaire '+usr1.cleaned_data['firstname']+' '+usr1.cleaned_data['lastname'], 'info@sep2015e.com', [usr2.cleaned_data['email']], fail_silently=False)

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
        emailForm1 = EmailOldUserForm(prefix="email1")
        emailForm2 = EmailOldUserForm(prefix="email2") 

        trn_open = Tournament.objects.filter(is_open=True).count()

        if trn_open == 0  :
            return render(request, 'players/no_tournament_open.html')
        else:

            return render(request, 'players/register.html', {
                "usr1": usr1,
                "reg1": reg1,
                "usr2": usr2,
                "reg2": reg2,
                "trn": trn,
                "email1": emailForm1,
                "email2": emailForm2
            })

def filled_registration(request):
    if request.method == 'POST':
        emailForm1 = EmailOldUserForm(request.POST, prefix="email1")
        emailForm2 = EmailOldUserForm(request.POST, prefix="email2")
        usr1 = PlayerForm(prefix="usr1")
        reg1 = RegistrationForm(prefix="reg1")
        usr2 = PlayerForm(prefix="usr2")
        reg2 = RegistrationForm(prefix="reg2")
        trn = OpenTournamentChoiceForm()

        if emailForm1.is_valid():
            email1 = emailForm1.cleaned_data['email']
            usr1 = PlayerForm(player_email=email1, prefix="usr1")
        if emailForm2.is_valid():
            email2 = emailForm2.cleaned_data['email']
            usr2 = PlayerForm(player_email=email2, prefix="usr2")
        emailForm1 = EmailOldUserForm(prefix="email1")
        emailForm2 = EmailOldUserForm(prefix="email2")
        return render(request, 'players/register.html', {
            "usr1": usr1,
            "reg1": reg1,
            "usr2": usr2,
            "reg2": reg2,
            "trn": trn,
            "email1": emailForm1,
            "email2": emailForm2
            })

    return redirect('players.views.register')
