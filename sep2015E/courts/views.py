from django.shortcuts import render
from courts.forms import RegisterForm, OwnerCourtsForm
from django.http import HttpResponseRedirect
from courts.models import Court
from tournament.models import Match, Tournament
from django.core.mail import send_mail

def register(request):
    """ Method who receive requests (post/get) from register.html
        create a court on post request """
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = RegisterForm(request.POST, request.FILES)  # Nous reprenons les données

        if form.is_valid(): # Nous vérifions que les données envoyées sont valides

            new_court = Court(owner_firstname = form.cleaned_data['owner_firstname'],
                    owner_lastname = form.cleaned_data['owner_lastname'],
                    owner_address_street = form.cleaned_data['owner_address_street'],
                    owner_address_number = form.cleaned_data['owner_address_number'],
                    owner_address_box = form.cleaned_data['owner_address_box'],
                    city = form.cleaned_data['city'],
                    zipcode = form.cleaned_data['zipcode'],
                    email = form.cleaned_data['email'],
                    phone = form.cleaned_data['phone'],
                    address_street = form.cleaned_data['address_street'],
                    address_number = form.cleaned_data['address_number'],
                    address_box = form.cleaned_data['address_box'],
                    ground = form.cleaned_data['ground'],
                    cover = form.cleaned_data['cover'],
                    image = form.cleaned_data['image'],
                    comment_access = form.cleaned_data['comment_access'],
                    comment_desiderata = form.cleaned_data['comment_desiderata'],
                    available = form.cleaned_data['available'])
            new_court.save()

            send_mail('Your owner page', 'You will find informations about your court here : http://'+request.META['HTTP_HOST']+ \
                '/courts/'+form.cleaned_data['owner_firstname']+'_'+form.cleaned_data['owner_lastname']+'/byowner', 'info@sep2015e.com', [form.cleaned_data['email']], fail_silently=False)

            return render(request, 'courts/registration_success.html')

        form_owner = OwnerCourtsForm(request.POST)
        if form_owner.is_valid():
            #form_owner.cleaned_data['tournament'].close_registrations()
            return HttpResponseRedirect('/courts/'+form.cleaned_data['owner_firstname']+'_'+form.cleaned_data['owner_lastname']+'/byowner.html')

    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        form = RegisterForm()  # Nous créons un formulaire vide
        form_owner = OwnerCourtsForm()

        trn_open = Tournament.objects.filter(is_open=True).count()

        if trn_open == 0  :
            return render(request, 'players/no_tournament_open.html')


    return render(request, 'courts/register.html', {"form":form, "form_owner":form_owner})

def byowner(request, param):
    """ Method who receive get request from byowner.html
        this is an owner page to get the court informations """
    court_owner = param.replace("%20", " ")
    courts = Court.objects.filter(owner_firstname=court_owner.split("_")[0], owner_lastname=court_owner.split("_")[1])
    court_owner = param.replace("_", " ")

    match_list = []
    for val in courts:
        match_list.append(Match.objects.filter(court=val))


    return render(request, 'courts/byowner.html', { \
            'court_owner': court_owner,\
            'courts': courts,\
            'match_list': match_list\
            })
