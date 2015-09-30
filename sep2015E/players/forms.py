from django import forms
from players.models import User

class RegisterForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('firstname','lastname','address','city','country','zipcode','email','level',)