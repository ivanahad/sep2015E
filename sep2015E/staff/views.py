from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from datetime import datetime
from staff.models import Messages
from staff.forms import MessageForm, EditPlayerForm
from courts.models import Court
from players.models import User


def login_staff(request):
    """Login page for staff."""
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('staff.views.home')
            else:
                return HttpResponse("Your staff account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('staff/login.html', {}, context)

def logout_staff(request):
    """Logout for staff."""
    logout(request)
    return redirect('home.views.index')

def home(request):
    """Home page for staff members."""
    if not request.user.is_authenticated():
        return redirect('staff.views.login_staff')
    if request.method == 'POST':
        form_msg = MessageForm(request.POST, prefix="msg")
        if form_msg.is_valid():
            Messages(author = name, \
                    destinator = form_msg.cleaned_data['destinator'], \
                    title = form_msg.cleaned_data['title'], \
                    message = form_msg.cleaned_data['message']).save()
    form_msg = MessageForm(prefix="msg")
    messages = Messages.objects.all() #replace by a call destined to the current staff member
    name=request.user.username
    return render(request, 'staff/home.html', {\
            'name': name, \
            'date':datetime.now(), \
            'messages':messages, \
            'form_msg': form_msg,
            })

def courts(request):
    if not request.user.is_authenticated():
        return redirect('staff.views.login_staff')

    courts = Court.objects.all()

    return render(request, 'staff/courts.html', locals())

def players(request):
    """Page listing the players registered in the event."""
    if not request.user.is_authenticated():
        return redirect('staff.views.login_staff')

    players = User.objects.all()
    return render(request, 'staff/players.html', { \
        'players':players ,
        })

def particular_player(request, player_id):
    """Page showing information on a particular player."""
    if not request.user.is_authenticated():
        return redirect('staff.views.login_staff')

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
