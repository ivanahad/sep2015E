from django import forms
from django.forms.extras.widgets import Select
from tournament.models import Tournament
import tournament

class OpenTournamentChoiceForm(forms.Form):
    tournament = forms.ModelChoiceField( \
            queryset=Tournament.objects.filter(is_open=True), \
        )

class CreateTournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ["name", "category", "pool_size"]
