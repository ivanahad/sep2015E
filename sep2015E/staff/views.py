from math import ceil

from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.mail import send_mass_mail
from django.template import Library

from datetime import datetime

from staff.models import Messages
from staff.forms import MessageForm, MailListForm

from courts.models import Court

from players.models import User
from players.forms import PlayerForm



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

def mail_list(request):
    """Form to send a mass email to all users."""
    if not request.user.is_authenticated():
        return redirect('staff.views.login_staff')
    if request.method == 'POST':
        form = MailListForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['content']
            emitter = 'info@sep2015e.com'

            datatuples = [(subject, message, emitter, [u.email]) \
                    for u in User.objects.all()]

            send_mass_mail(datatuples)
            return HttpResponse("Email envoyé.<br/><a href=\"home\">Retour à l'accueil</a>")
    else:
        form = MailListForm()

    return render(request, 'staff/mail_list.html', {'form':form})

def courts(request):
    if not request.user.is_authenticated():
        return redirect('staff.views.login_staff')

    courts = Court.objects.all()

    return render(request, 'staff/courts.html', locals())

register = Library()

@register.filter
def get_range( value ):
    """
    Filter - returns a list containing range made from given value
    """
    return range( value )

def players(request, page_id):
    """Page listing the players registered in the event."""
    if not request.user.is_authenticated():
        return redirect('staff.views.login_staff')

    players_per_page = 10   #Number of players displayed by page

    number_players = User.objects.count()
    number_pages = ceil(number_players/players_per_page) #Number of pages for the navbar

    extremity1 = 0+(int(page_id)-1)*players_per_page    #Range
    extremity2 = (int(page_id)*players_per_page)-1
    players = User.objects.order_by('lastname', 'firstname').all()[extremity1:extremity2]

    return render(request, 'staff/players.html', { \
        'players':players ,
        'page_id':int(page_id),
        'number_pages':number_pages,
        'n':range(1, number_pages+1),
        'prev':int(page_id)-1,
        'next':int(page_id)+1,
        })

def particular_player(request, player_id):
    """Page showing information on a particular player."""
    if not request.user.is_authenticated():
        return redirect('staff.views.login_staff')

    if request.method == 'POST':
        form=PlayerForm(request.POST, player_id=player_id)
        print(form)
        if not form.is_valid():
            player = User.objects.filter(id=player_id).get()
            player.firstname=form.cleaned_data['firstname']
            player.lastname=form.cleaned_data['lastname']
            player.address_street=form.cleaned_data['address_street']
            player.address_number=form.cleaned_data['address_number']
            player.city=form.cleaned_data['city']
            player.country=form.cleaned_data['country']
            player.zipcode=form.cleaned_data['zipcode']
            player.email=form.cleaned_data['email']
            player.phone=form.cleaned_data['phone']
            player.save()
            return redirect('staff.views.players')
    else:
        player = User.objects.filter(id=player_id).get()
        form = PlayerForm(player_id=player.id)
        return render(request, 'staff/particular_player.html', { \
            'player':player, \
            'form':form,
            })
