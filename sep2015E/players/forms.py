from django import forms
from players.models import User

class RegisterForm(forms.ModelForm):
	class Meta:
		model = User
		fields = '__all__'
		prefix = 'form1'