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
        fields='__all__'

    def __init__(self, *args, **kwargs):
        super(MatchEditForm, self).__init__(*args, **kwargs)
        self.fields['team1'].widget.attrs['readonly'] = True
        self.fields['team2'].widget.attrs['readonly'] = True

    def clean_team1(self):
        return self.cleaned_data['team1']

    def clean_team2(self):
        return self.cleaned_data['team2']
