from django.shortcuts import render
from courts.forms import RegisterForm, OwnerCourtsForm
from django.http import HttpResponseRedirect
from courts.models import Court
from tournament.models import Match
from django.core.mail import send_mail

def register(request):
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = RegisterForm(request.POST, request.FILES)  # Nous reprenons les données

        if form.is_valid(): # Nous vérifions que les données envoyées sont valides

            new_court = Court(owner = form.cleaned_data['owner'], address = form.cleaned_data['address'], city = form.cleaned_data['city'],
            zipcode = form.cleaned_data['zipcode'], email = form.cleaned_data['email'], phone = form.cleaned_data['phone'],
            ground = form.cleaned_data['ground'], cover = form.cleaned_data['cover'], image = form.cleaned_data['image'],
            comment_access = form.cleaned_data['comment_access'], comment_desiderata = form.cleaned_data['comment_desiderata'],
            available = form.cleaned_data['available'])
            new_court.save()

            send_mail('Your owner page', 'You will find informations about your court here : http://'+request.META['HTTP_HOST']+ \
                '/courts/'+form.cleaned_data['owner']+'/byowner', 'info@sep2015e.com', [form.cleaned_data['email']], fail_silently=False)

            return HttpResponseRedirect('/')

        form_owner = OwnerCourtsForm(request.POST, prefix="ownerform")
        if form_owner.is_valid():
            #form_owner.cleaned_data['tournament'].close_registrations()
            return HttpResponseRedirect('/courts/'+form_owner.cleaned_data['owner']+'/byowner.html')

    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        form = RegisterForm()  # Nous créons un formulaire vide
        form_owner = OwnerCourtsForm(prefix="ownerform")

    return render(request, 'courts/register.html', locals())

def byowner(request, param):
    court_owner = param
    courts = Court.objects.filter(owner=param)
    match_list = []
    for val in courts:
        match_list.append(Match.objects.filter(court=val))


    return render(request, 'courts/byowner.html', { \
            'court_owner': court_owner,\
            'match_list': match_list\
            })
