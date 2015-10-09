from django import forms
from django.forms.extras.widgets import Select
from tournament.models import Tournament
import tournament

class LaunchTournamentForm(forms.Form):
    tournament = forms.ModelChoiceField( \
            queryset=Tournament.objects.filter(is_open=True), \
            empty_label=None)
