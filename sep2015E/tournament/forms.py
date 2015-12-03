from django import forms
from django.forms.extras.widgets import Select
from django.db.models import Q
from tournament.models import Tournament, Match, PoolParticipant, Pool
from courts.models import Court
from players.models import User, Pair
import tournament

class OpenTournamentChoiceForm(forms.Form):
    tournament = forms.ModelChoiceField( \
            queryset=Tournament.objects.filter(is_open=True), \
            empty_label=None, \
        )

class CreateTournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ["name", "category", "pool_size", "mixte"]

class MatchEditForm(forms.ModelForm):
    class Meta:
        model = Match
        fields=["score1", "score2", "court"]

class AssignCourtForm(forms.Form):
    court = forms.ModelChoiceField( \
            queryset=Court.objects.all(), \
            empty_label=None, \
        )

class AssignPoolLeaderForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.pool_id = kwargs.pop('pool_id')
        super(AssignPoolLeaderForm,self).__init__(*args,**kwargs)
        pool = Pool.objects.get(pk=self.pool_id)
        self.fields['leader'] = forms.ModelChoiceField( \
                queryset=User.objects.all().order_by("lastname", "firstname"), \
                empty_label=None, \
            )

    leader = forms.ModelChoiceField( \
            queryset=User.objects.all(), \
            empty_label=None, \
        )

class AssignDateForm(forms.Form):
    date = forms.DateTimeField()
