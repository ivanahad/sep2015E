from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.conf import settings
from players.forms import PlayerForm, RegistrationForm, PairRegistrationForm, EmailOldUserForm
from players.models import User, Pair, UserRegistration
from tournament.forms import OpenTournamentChoiceForm
from tournament.models import TournamentParticipant, SoloParticipant, Tournament
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime


#send_mail('Enregistrement à un tournoi', 'Bonjour '+usr1.cleaned_data['firstname']+' '+usr1.cleaned_data['lastname']+',\n\nAsmae vous confirme que vous avez bien été inscrit au tournoi ' \
#    +trn.cleaned_data['tournament'].name+' '+trn.cleaned_data['tournament'].category+' avec votre partenaire '+usr2.cleaned_data['firstname']+' '+usr2.cleaned_data['lastname'], 'info@sep2015e.com', [usr1.cleaned_data['email']], fail_silently=False)

#send_mail('Enregistrement à un tournoi', 'Bonjour '+usr2.cleaned_data['firstname']+' '+usr2.cleaned_data['lastname']+',\n\nAsmae vous confirme que vous avez bien été inscrit au tournoi ' \
#    +trn.cleaned_data['tournament'].name+' '+trn.cleaned_data['tournament'].category+' avec votre partenaire '+usr1.cleaned_data['firstname']+' '+usr1.cleaned_data['lastname'], 'info@sep2015e.com', [usr2.cleaned_data['email']], fail_silently=False)

def register(request):
    """ Method who receive requests (post/get) from register.html
        create a player on post request """
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        usr1 = PlayerForm(request.POST, prefix="usr1")
        reg1 = RegistrationForm(request.POST, prefix="reg1")
        usr2 = PlayerForm(request.POST, prefix="usr2")
        reg2 = RegistrationForm(request.POST, prefix="reg2")
        pair = PairRegistrationForm(request.POST)

        emailForm1 = EmailOldUserForm(prefix="email1")
        emailForm2 = EmailOldUserForm(prefix="email2")

        #Solo registration
        if 'solo_registration' in request.POST \
                and usr1.is_valid() and reg1.is_valid():
            new_user1 = User( \
                    firstname = usr1.cleaned_data['firstname'], \
                    lastname = usr1.cleaned_data['lastname'], \
                    gender = usr1.cleaned_data['gender'], \
                    birthdate = usr1.cleaned_data['birthdate'], \
                    address_street = usr1.cleaned_data['address_street'], \
                    address_number = usr1.cleaned_data['address_number'], \
                    address_box = usr1.cleaned_data['address_box'], \
                    city = usr1.cleaned_data['city'], \
                    country = usr1.cleaned_data['country'], \
                    zipcode = usr1.cleaned_data['zipcode'], \
                    email = usr1.cleaned_data['email'], \
                    phone = usr1.cleaned_data['phone'])
            new_user1.save()

            registration1 = UserRegistration( \
                    user = new_user1, \
                    season = settings.CURRENT_SEASON, \
                    bbq = reg1.cleaned_data['bbq'], \
                    level = reg1.cleaned_data['level'])
            registration1.save()

            assign_tournament_solo(new_user1)

            return redirect('players.views.payement', id_user1=new_user1.pk, id_registration1=registration1.pk,
                    id_user2=-1, id_registration2=-1, id_pair=-1)

        #Pair registration
        elif usr1.is_valid() and usr2.is_valid() \
                and reg1.is_valid() and reg2.is_valid() \
                and pair.is_valid():
            new_user1 = User( \
                    firstname = usr1.cleaned_data['firstname'], \
                    lastname = usr1.cleaned_data['lastname'], \
                    gender = usr1.cleaned_data['gender'], \
                    birthdate = usr1.cleaned_data['birthdate'], \
                    address_street = usr1.cleaned_data['address_street'], \
                    address_number = usr1.cleaned_data['address_number'], \
                    address_box = usr1.cleaned_data['address_box'], \
                    city = usr1.cleaned_data['city'], \
                    country = usr1.cleaned_data['country'], \
                    zipcode = usr1.cleaned_data['zipcode'], \
                    email = usr1.cleaned_data['email'], \
                    phone = usr1.cleaned_data['phone'])
            new_user1.save()

            registration1 = UserRegistration( \
                    user = new_user1, \
                    season = settings.CURRENT_SEASON, \
                    bbq = reg1.cleaned_data['bbq'], \
                    level = reg1.cleaned_data['level'])
            registration1.save()

            new_user2 = User( \
                    firstname = usr2.cleaned_data['firstname'], \
                    lastname = usr2.cleaned_data['lastname'], \
                    gender = usr2.cleaned_data['gender'], \
                    birthdate = usr2.cleaned_data['birthdate'], \
                    address_street = usr2.cleaned_data['address_street'], \
                    address_number = usr2.cleaned_data['address_number'], \
                    address_box = usr2.cleaned_data['address_box'], \
                    city = usr2.cleaned_data['city'], \
                    country = usr2.cleaned_data['country'], \
                    zipcode = usr2.cleaned_data['zipcode'], \
                    email = usr2.cleaned_data['email'], \
                    phone = usr2.cleaned_data['phone'])
            new_user2.save()

            registration2 = UserRegistration( \
                    user = new_user2, \
                    season = settings.CURRENT_SEASON, \
                    bbq = reg2.cleaned_data['bbq'], \
                    level = reg2.cleaned_data['level'])
            registration2.save()

            pair = Pair(player1 = new_user1, player2 = new_user2, \
                    average = 0.0, \
                    season = settings.CURRENT_SEASON, \
                    comment = pair.cleaned_data['comment'])
            pair.save()

            assign_tournament(pair)

            return redirect('players.views.payement', id_user1=new_user1.pk, id_user2=new_user2.pk,
                id_registration1=registration1.pk, id_registration2=registration2.pk, id_pair=pair.pk)

    else:
        usr1 = PlayerForm(prefix="usr1")
        reg1 = RegistrationForm(prefix="reg1")
        usr2 = PlayerForm(prefix="usr2")
        reg2 = RegistrationForm(prefix="reg2")
        pair = PairRegistrationForm()
        emailForm1 = EmailOldUserForm(prefix="email1")
        emailForm2 = EmailOldUserForm(prefix="email2")

        trn_open = Tournament.objects.filter(is_open=True).count()

        if trn_open == 0  :
            return render(request, 'players/no_tournament_open.html')

    return render(request, 'players/register.html', {
        "usr1": usr1,
        "reg1": reg1,
        "usr2": usr2,
        "reg2": reg2,
        "pair": pair,
        "email1": emailForm1,
        "email2": emailForm2
            })

def assign_tournament_solo(player):
    """ Register a player solo for a tournament if it exists based on his gender and age"""
    #Assign the category based on birthdate
    current_year = datetime.now().year
    player_birth_year = player.birthdate.year
    smaller_difference = current_year - player_birth_year

    if player.gender == "M":
        mixte = "M"
    else:
        mixte = "F"

    category = "none"
    if smaller_difference <= 10 and smaller_difference >=9:
        category = "preminimes"
    elif smaller_difference <= 12 and smaller_difference >=11:
        category = "minimes"
    elif smaller_difference <= 14 and smaller_difference >=13:
        category = "cadets"
    elif smaller_difference <= 16 and smaller_difference >=15:
        category = "scolaires"
    elif smaller_difference <= 19 and smaller_difference >=17:
        category = "juniors"
    elif smaller_difference <= 40 and smaller_difference >=20:
        category = "seniors"
    elif smaller_difference > 40:
        category = 'elites'

    #Assign a tournament if possible
    exist = (Tournament.objects.filter(category=category, mixte=mixte, season=settings.CURRENT_SEASON).count() != 0)
    if exist:
        tournament= Tournament.objects.get(category=category, mixte=mixte, season=settings.CURRENT_SEASON)
        tp = SoloParticipant(player=player, tournament=tournament)
        tp.save()
    else:
        tp = SoloParticipant(player=player)
        tp.save()

def assign_tournament(pair):
    """ Assign a tournament to a pair based on their genders (if same or different)
        and their birthdate. The category is based on the older player.
        It may happen that some players are not assigned tournaments (don'f fit)."""
    player1 = pair.player1
    player2 = pair.player2

    #Check if mixte
    if player1.gender != player2.gender:
        mixte = "Mixte"
    elif player1.gender == "M":
        mixte = "M"
    else:
        mixte = "F"

    #Assign the category based on birthdate
    current_year = datetime.now().year
    player1_birth_year = player1.birthdate.year
    player2_birth_year = player2.birthdate.year
    smaller_difference = current_year - player1_birth_year
    if current_year - player2_birth_year < current_year - player1_birth_year:
        smaller_difference = current_year - player2_birth_year

    category = "none"
    if smaller_difference <= 10 and smaller_difference >=9:
        category = "preminimes"
    elif smaller_difference <= 12 and smaller_difference >=11:
        category = "minimes"
    elif smaller_difference <= 14 and smaller_difference >=13:
        category = "cadets"
    elif smaller_difference <= 16 and smaller_difference >=15:
        category = "scolaires"
    elif smaller_difference <= 19 and smaller_difference >=17:
        category = "juniors"
    elif smaller_difference <= 40 and smaller_difference >=20:
        category = "seniors"
    elif smaller_difference > 40:
        category = 'elites'

    if current_year - player1_birth_year <= 15:
        if current_year - player2_birth_year >= 25:
            category = "familles"
            mixte = True
    elif current_year - player2_birth_year <= 15:
        if current_year - player1_birth_year >= 25:
            category = "familles"
            mixte = True

    #Assign a tournament if possible
    exist = (Tournament.objects.filter(category=category, mixte=mixte, season=settings.CURRENT_SEASON).count() != 0)
    if exist:
        tournament= Tournament.objects.get(category=category, mixte=mixte, season=settings.CURRENT_SEASON)
        tp = TournamentParticipant(participant=pair, tournament=tournament)
        tp.save()

def unregister(request):
    """ Request to delete all the data of a player on the database """
    form = EmailOldUserForm()

    if request.method == 'POST':
        form = EmailOldUserForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data['email'])
                send_mail('Suppression de votre adresse sur le site SEP2015E', "Vous avez demandé que votre adresse soit supprimée de notre base de données. Si vous êtes certain de votre choix, cliquez sur le lien suivant ou copiez-collez le dans votre navigateur.\n\nhttp://"+request.META['HTTP_HOST']+"/players/unregister_confirm?user="+str(user.pk)+"&token="+str(hash(user))+"\n\nSi vous n'avez pas demandé à ce que votre adresse soit supprimée, veuillez ignorer ce message.", 'info@sep2015e.com', [user.email], fail_silently=False)
                return HttpResponseRedirect("/")
            except ObjectDoesNotExist:
                form.add_error('email', "Cette adresse n'est pas présente dans notre base de données.")

    return render(request, 'players/unregister.html', {\
            'form_email': form, \
            })

def unregister_confirm(request):
    """ Confirmation to delete all the data of a player on the database """
    user_pk = request.GET.get('user', -1)
    token = request.GET.get('token', -1)
    user = User.objects.get(pk=int(user_pk))
    if hash(user) == int(token):
        user.delete()
        return render(request, 'players/unregister_success.html')
    else:
        return render(request, 'players/unregister_failure.html')

def filled_registration(request):
    """Registration already filled for participants on previous years."""
    if request.method == 'POST':
        emailForm1 = EmailOldUserForm(request.POST, prefix="email1")
        usr1 = PlayerForm(prefix="usr1")
        reg1 = RegistrationForm(prefix="reg1")
        usr2 = PlayerForm(prefix="usr2")
        reg2 = RegistrationForm(prefix="reg2")
        trn = OpenTournamentChoiceForm()

        if emailForm1.is_valid():
            try:
                oldusr = User.objects.get(email=emailForm1.cleaned_data['email'])
            except ObjectDoesNotExist:
                return render(request, 'players/register.html', {
                        "usr1": usr1,
                        "reg1": reg1,
                        "usr2": usr2,
                        "reg2": reg2,
                        "trn": trn,
                        "email1": emailForm1,
                        "email2": emailForm2
                        })
            send_mail('Enregistrement tournoi Asmae', 'Confirmez votre inscription au tournoi ici : http://'+request.META['HTTP_HOST']+ \
                '/players/fregister?email=%s&token=%s' % (oldusr.email, str(hash(oldusr))), 'info@sep2015e.com', [emailForm1.cleaned_data['email']], fail_silently=False)
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
    else:
        email = request.GET.get('email', None)
        token = request.GET.get('token', None)
        usr1 = PlayerForm(prefix="usr1")
        if email != None and token != None:
            try:
                oldusr = User.objects.get(email=email)
                if hash(oldusr) == int(token):
                    usr1 = PlayerForm(player_email=email, prefix="usr1")
            except ObjectDoesNotExist:
                pass
        reg1 = RegistrationForm(prefix="reg1")
        usr2 = PlayerForm(prefix="usr2")
        reg2 = RegistrationForm(prefix="reg2")
        trn = OpenTournamentChoiceForm()
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


def payement(request, id_user1, id_registration1, id_registration2, id_user2, id_pair):
    """ Method who receive requests (post/get) from payment.html
        create a user on post request """
    user1 = UserRegistration.objects.get(pk=id_registration1)
    if int(id_user2) != -1:
        nb_user = 2
        user2 = UserRegistration.objects.get(pk=id_registration2)

        if user1.bbq is True and user2.bbq is True:
            nb_bbq = 2
        elif user1.bbq is True or user2.bbq is True:
            nb_bbq = 1
        else:
            nb_bbq = 0
    else:
        nb_user = 1

        if user1.bbq is True:
            nb_bbq = 1
        else:
            nb_bbq = 0

    total = nb_user*20 + nb_bbq*15
    error = False

    if request.method == 'POST':
        if 'delete' in request.POST:
            UserRegistration.objects.get(pk=id_registration1).delete()
            User.objects.get(pk=id_user1).delete()
            if int(id_user2) != -1:
                Pair.objects.get(pk=id_pair).delete()
                UserRegistration.objects.get(pk=id_registration2).delete()
                User.objects.get(pk=id_user2).delete()
                return redirect('plays.views.register')
            return redirect('players.views.register')
        else:
            payement_method = request.POST.get('payement_method', False)
            if payement_method is False:
                error = True
                return render(request, 'players/payement.html', {
                    "user":id_user1,
                    "other_user": id_user2,
                    "reg":id_registration1,
                    "reg2":id_registration2,
                    "nb_user": nb_user,
                    "nb_bbq": nb_bbq,
                    "total": total,
                    "error": error
                })
            user1.payement_method = payement_method
            user1.save()

            #send_mail('Enregistrement à un tournoi', 'Bonjour '+usr1.cleaned_data['firstname']+' '+usr1.cleaned_data['lastname']+',\n\nAsmae vous confirme que vous avez bien été inscrit au tournoi ' \
            #    +trn.cleaned_data['tournament'].name+' '+trn.cleaned_data['tournament'].category, 'info@sep2015e.com', [usr1.cleaned_data['email']], fail_silently=False)

            if int(id_user2) != -1:
                user2.payement_method = payement_method
                user2.save()
            return render(request, 'players/registration_success.html')

    return render(request, 'players/payement.html', {
        "user":id_user1,
        "other_user": id_user2,
        "reg":id_registration1,
        "reg2":id_registration2,
        "nb_user": nb_user,
        "nb_bbq": nb_bbq,
        "total": total,
        "error": error
    })
