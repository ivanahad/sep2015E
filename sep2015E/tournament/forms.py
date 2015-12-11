from django import forms
from django.forms.extras.widgets import Select
from django.db.models import Q
from tournament.models import Tournament, Match, PoolParticipant, Pool
from courts.models import Court
from players.models import User, Pair
import tournament
from staff.models import Staff

class OpenTournamentChoiceForm(forms.Form):
    """ Form to choose a tournament """
    tournament = forms.ModelChoiceField( \
            queryset=Tournament.objects.filter(is_open=True), \
            empty_label=None, \
        )

class CreateTournamentForm(forms.ModelForm):
    """ Form to create a tournament """
    class Meta:
        model = Tournament
        fields = ["name", "category", "pool_size", "mixte"]

class MatchEditForm(forms.ModelForm):
    """ Form to edit a match """
    class Meta:
        model = Match
        fields=["score1", "score2", "court"]

class BracketMatchEditForm(forms.ModelForm):
    """ Form to edit a match """
    matchId = forms.IntegerField()

    class Meta:
        model = Match
        fields=["score1", "score2", "court"]
    def save(self, commit=True):
        # do something with self.cleaned_data['temp_id']
        return super(BracketMatchEditForm, self).save(commit=commit)

class AssignCourtForm(forms.Form):
    """ Form to assign a court to a match """
    court = forms.ModelChoiceField( \
            queryset=Court.objects.all(), \
            empty_label=None, \
        )

class AssignPoolLeaderForm(forms.Form):
    """ Form to assign a leader to the pool """
    def __init__(self,*args,**kwargs):
        self.pool_id = kwargs.pop('pool_id')
        super(AssignPoolLeaderForm,self).__init__(*args,**kwargs)
        pool = Pool.objects.get(pk=self.pool_id)
        pool_participants = PoolParticipant.objects.filter(pool=pool)
        players1 = Pair.objects.filter(poolparticipant=pool_participants).only('player1')
        players2 = Pair.objects.filter(poolparticipant=pool_participants).only('player2')
        self.fields['leader'] = forms.ModelChoiceField( \
                queryset=User.objects.filter(Q(player1=players1) | Q(player2=players2)).order_by("lastname", "firstname"), \
                empty_label=None, \
            )

    leader = forms.ModelChoiceField( \
            queryset=User.objects.all(), \
            empty_label=None, \
        )

class AssignDateForm(forms.Form):
    date = forms.DateTimeField()

class AssignStaffForm(forms.Form):
    staff = forms.ModelChoiceField( \
            queryset=Staff.objects.all(), \
            empty_label=None, \
        )
