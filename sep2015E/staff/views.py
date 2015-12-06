from math import ceil
import os

from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.mail import send_mass_mail
from django.db.models import Q
from django.core.servers.basehttp import FileWrapper
from django.contrib.admin.models import LogEntry
from django.conf import settings


from datetime import datetime

from staff.models import Messages, Files, Staff
from staff.forms import MessageForm, MailListForm, FilesForm, SearchForm

from courts.models import Court

from players.models import User, Pair, UserRegistration
from players.forms import PlayerForm, RegistrationForm, AssignPairForm

from tournament.models import TournamentParticipant, Tournament, SoloParticipant



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

    name=request.user.username

    form_files = FilesForm(prefix="files")
    form_msg = MessageForm(prefix="msg")

    if request.method == 'POST':
        #Form for messages
        if 'type_msg' in request.POST:
            form_msg = MessageForm(request.POST, prefix="msg")
            if form_msg.is_valid():
                Messages(author = request.user, \
                        title = form_msg.cleaned_data['title'], \
                        message = form_msg.cleaned_data['message']).save()
                return HttpResponseRedirect('/staff/home')
        #Form for files
        if 'type_files' in request.POST:
            form_files = FilesForm(request.POST, request.FILES, prefix="files")
            if form_files.is_valid():
                Files(name=form_files.cleaned_data['name'], \
                    f=form_files.cleaned_data['f'], owner=request.user).save()
                return HttpResponseRedirect('/staff/home')

    messages = Messages.objects.all()
    files = Files.objects.all()

    return render(request, 'staff/home.html', {\
            'name': name, \
            'date':datetime.now(), \
            'messages':messages, \
            'form_msg': form_msg,
            'form_files': form_files,
            'files' : files,
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
    """ Page listing all the courts"""
    if not request.user.is_authenticated():
        return redirect('staff.views.login_staff')

    courts = Court.objects.all()

    return render(request, 'staff/courts.html', locals())


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

def pairless_players(request, page_id):
    """Page listing the players registered in the event."""
    if not request.user.is_authenticated():
        return redirect('staff.views.login_staff')

    players_per_page = 10   #Number of players displayed by page

    number_players = SoloParticipant.objects.all().count()
    number_pages = ceil(number_players/players_per_page) #Number of pages for the navbar

    extremity1 = 0+(int(page_id)-1)*players_per_page    #Range
    extremity2 = (int(page_id)*players_per_page)-1
    players = SoloParticipant.objects.all()[extremity1:extremity2]

    return render(request, 'staff/pairless_players.html', { \
        'players':players ,
        'page_id':int(page_id),
        'number_pages':number_pages,
        'n':range(1, number_pages+1),
        'prev':int(page_id)-1,
        'next':int(page_id)+1,
        })

def tournamentless_pairs(request, page_id):
    """Page listing the players registered in the event
        that are not assigned to a tournament."""
    if not request.user.is_authenticated():
        return redirect('staff.views.login_staff')

    pairs_per_page = 10   #Number of players displayed by page
    tournament_participants = TournamentParticipant.objects.all()
    number_pairs = Pair.objects.exclude(tournamentparticipant=tournament_participants).count()
    number_pages = ceil(number_pairs/pairs_per_page) #Number of pages for the navbar

    extremity1 = 0+(int(page_id)-1)*pairs_per_page    #Range
    extremity2 = (int(page_id)*pairs_per_page)-1
    pairs = Pair.objects.exclude(tournamentparticipant=tournament_participants)[extremity1:extremity2]

    return render(request, 'staff/tournamentless_pairs.html', { \
        'pairs':pairs ,
        'page_id':int(page_id),
        'number_pages':number_pages,
        'n':range(1, number_pages+1),
        'prev':int(page_id)-1,
        'next':int(page_id)+1,
        })

def particular_player(request, page_id, player_id):
    """Page showing information for a particular player."""
    players_per_page = 10   #Number of players displayed by page

    number_players = User.objects.count()
    number_pages = ceil(number_players/players_per_page) #Number of pages for the navbar

    extremity1 = 0+(int(page_id)-1)*players_per_page    #Range
    extremity2 = (int(page_id)*players_per_page)-1
    players = User.objects.order_by('lastname', 'firstname').all()[extremity1:extremity2]
    player = User.objects.filter(id=player_id).get()


    if not request.user.is_authenticated():
        return redirect('staff.views.login_staff')

    if request.method == 'POST':
        player = get_object_or_404(User, pk=player_id)
        form = PlayerForm(request.POST, player_id=player_id, instance=player)
        user_reg = get_object_or_404(UserRegistration, user=player, season=settings.CURRENT_SEASON)
        reg_form = RegistrationForm(request.POST, user_reg_id=user_reg.pk, instance=user_reg)
        pair_form = AssignPairForm(request.POST)
        if pair_form.is_valid():
            other_player=pair_form.cleaned_data['other_player']
            solo = SoloParticipant.objects.get(player=player)
            solo.delete()
            SoloParticipant.objects.get(player=other_player).delete()
            Pair(player1=player, player2=other_player.player, average=0, season=settings.CURRENT_SEASON).save()
        if form.is_valid():
            obj = form.save()
        if reg_form.is_valid():
            obj2 = reg_form.save()
    player_pairs = Pair.objects.filter(season=settings.CURRENT_SEASON).filter(Q(player1=player) | Q(player2=player))
    if player_pairs.count() == 0:
        player_pairs=None
    user_reg = UserRegistration.objects.get(user=player, season=settings.CURRENT_SEASON)
    form = PlayerForm(player_id=player.id)
    reg_form = RegistrationForm(user_reg_id = user_reg.pk)
    pair_form = AssignPairForm()
    return render(request, 'staff/particular_player.html', { \
        'player':player, \
        'form':form,
        'players':players ,
        'player_pairs': player_pairs,
        'page_id':int(page_id),
        'number_pages':number_pages,
        'n':range(1, number_pages+1),
        'prev':int(page_id)-1,
        'next':int(page_id)+1,
        'reg_form': reg_form,
        'pair_form':pair_form
        })




def particular_pair(request, id_pair):
    pair = Pair.objects.get(pk=id_pair)
    tournament = None
    all_tournaments = Tournament.objects.all()
    if TournamentParticipant.objects.filter(participant=pair).count() != 0:
        tournament = TournamentParticipant.objects.filter(participant=pair).get().tournament
    if request.method == 'POST':
        new_tournament = request.POST['tournament'].strip()
        new_tournament = Tournament.objects.get(pk=int(new_tournament))
        if tournament != None:
            tournament_participant = TournamentParticipant.objects.get(participant=pair, tournament=tournament)
            tournament_participant.delete()
        tournament_participant = TournamentParticipant(tournament=new_tournament, participant=pair)
        tournament_participant.save()
        tournament = new_tournament

    return render(request, 'staff/particular_pair.html', { \
        'pair':pair,
        'tournament':tournament,
        'all_tournaments': all_tournaments,
        })

def search(request):
    """Search staff or owners of courts"""
    if request.method == 'POST':
        query = request.POST['query'].strip()
        players = User.objects.filter(Q(firstname__contains=query) | Q(lastname__contains=query))
        owners = Court.objects.filter(Q(owner_firstname__contains=query) | Q(owner_lastname__contains=query))
        form = SearchForm()
        return render(request, 'staff/search.html', { \
            'players':players,
            'owners':owners,
            'query':query,
            'form':form,
        })
    else:
        return redirect('staff.views.home')

def advanced_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        query=""
        if form.is_valid():
            users = User.objects.all()
            owners = Court.objects.all()
            #Filter by name
            name = form.cleaned_data['name']
            query=name
            users = users.filter(Q(firstname__contains=query) | Q(lastname__contains=query))
            owners = owners.filter(owner__contains=query)
            #Filter by gender
            gender = form.cleaned_data['gender']
            if gender != 'A':
                users=users.filter(gender=gender)
            #Filter by birthdate
            birthdate_equality=form.cleaned_data['birthdate_equality']
            birthdate = form.cleaned_data['birthdate']
            if birthdate != None:
                if birthdate_equality == ">":
                    users=users.filter(birthdate__gte=birthdate)
                elif birthdate_equality == "<":
                    users=users.filter(birthdate__lte=birthdate)
                else:
                    users=users.filter(birthdate=birthdate)
            #Filter by is in pair or not
            in_pair = form.cleaned_data['in_pair']
            if in_pair=="T":
                solo = SoloParticipant.objects.all()
                users=users.exclude(soloparticipant=solo)
            elif in_pair=="F":
                solo = SoloParticipant.objects.all()
                users=users.filter(soloparticipant=solo)
            #Filter is in tournament or not
            in_tournament= form.cleaned_data['in_tournament']
            if in_tournament=="T":
                tournament_participants = TournamentParticipant.objects.all()
                pairs = Pair.objects.exclude(tournamentparticipant=tournament_participants).only('player1')
                users=users.exclude(player1=pairs)
                pairs = Pair.objects.exclude(tournamentparticipant=tournament_participants).only('player2')
                users=users.exclude(player2=pairs)
            elif in_tournament=="F":
                tournament_participants = TournamentParticipant.objects.all()
                pairs = Pair.objects.exclude(tournamentparticipant=tournament_participants).only('player1')
                users=users.filter(player1=pairs)
                pairs = Pair.objects.exclude(tournamentparticipant=tournament_participants).only('player2')
                users=users.filter(player2=pairs)

            return render(request, 'staff/search.html', { \
                'players':users,
                'owners':owners,
                'query':query,
                'form':form,
            })

    return redirect('staff.views.home')

def send_file(request, id_file):
    """Send a file"""
    f=Files.objects.get(pk=id_file)
    response = HttpResponse(f.f, content_type='none')
    response['Content-Disposition'] = 'attachment; filename=' + '"' + str(f.f) + '"'
    return response
