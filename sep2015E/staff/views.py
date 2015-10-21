from django.shortcuts import render, redirect
from datetime import datetime
from staff.models import Messages
from staff.forms import MessageForm, EditPlayerForm
from courts.models import Court
from players.models import User


name = "Eric Duvoie" #replace by a call to database


def home(request):
    """Home page for staff members."""

    if request.method == 'POST':

        form_msg = MessageForm(request.POST, prefix="msg")
        if form_msg.is_valid():
            Messages(author = name, \
                    destinator = form_msg.cleaned_data['destinator'], \
                    title = form_msg.cleaned_data['title'], \
                    message = form_msg.cleaned_data['message']).save()
    form_msg = MessageForm(prefix="msg")
    messages = Messages.objects.all() #replace by a call destined to the current staff member

    return render(request, 'staff/home.html', {\
            'name': name, \
            'date':datetime.now(), \
            'messages':messages, \
            'form_msg': form_msg,
            })

def courts(request):
    courts = Court.objects.all()

    return render(request, 'staff/courts.html', locals())

def players(request):
    players = User.objects.all()
    return render(request, 'staff/players.html', { \
        'players':players ,
        })

def particular_player(request, player_id):
    if request.method == 'POST':
        form=EditPlayerForm(request.POST, player_id=player_id)
        if form.is_valid():
            player = User.objects.filter(id=player_id).get()
            player.firstname=form.cleaned_data['firstname']
            player.lastname=form.cleaned_data['lastname']
            player.address=form.cleaned_data['address']
            player.city=form.cleaned_data['city']
            player.country=form.cleaned_data['country']
            player.zipcode=form.cleaned_data['zipcode']
            player.email=form.cleaned_data['email']
            player.phone=form.cleaned_data['phone']
            player.save()
            return redirect('staff.views.players')
    else:
        player = User.objects.filter(id=player_id).get()
        form = EditPlayerForm(player_id=player.id)
        return render(request, 'staff/particular_player.html', { \
            'player':player, \
            'form':form,
            })
