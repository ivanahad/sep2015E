from django import forms
from django.forms.extras.widgets import Select
from tournament.models import Tournament, Match
import tournament

class OpenTournamentChoiceForm(forms.Form):
    tournament = forms.ModelChoiceField( \
            queryset=Tournament.objects.filter(is_open=True), \
            empty_label=None, \
        )

class CreateTournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ["name", "category", "pool_size"]

class MatchEditForm(forms.ModelForm):
    class Meta:
        model = Match
        fields=["score1", "score2", "court"]
