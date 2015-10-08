from django.shortcuts import render
from courts.forms import RegisterForm
from django.http import HttpResponseRedirect
from courts.models import Court

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

            return HttpResponseRedirect('/')

    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        form = RegisterForm()  # Nous créons un formulaire vide

    return render(request, 'courts/register.html', locals())
