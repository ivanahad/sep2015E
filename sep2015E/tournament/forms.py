from django import forms
import tournament

class LaunchTournamentForm(forms.ModelForm):
	class Meta:
		model = tournament.models.Tournament
		fields = ['name']
