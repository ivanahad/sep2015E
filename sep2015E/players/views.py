from django.shortcuts import render
from players.forms import RegisterForm

def register(request):
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = RegisterForm(request.POST)  # Nous reprenons les données

        if form.is_valid(): # Nous vérifions que les données envoyées sont valides

            # Ici nous pouvons traiter les données du formulaire
            nom = form.cleaned_data['nom']
            commentaire = form.cleaned_data['commentaire']
            email = form.cleaned_data['email']

    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        form = RegisterForm()  # Nous créons un formulaire vide

    return render(request, 'players/register.html', locals())
