from django import forms
from django.forms.extras.widgets import Select
from tournament.models import Tournament, Match
from courts.models import Court
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
