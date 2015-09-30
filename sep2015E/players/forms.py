from django import forms

class RegisterForm(forms.Form):
	name = forms.CharField(max_length=100)
	commentaire = forms.CharField(widget=forms.Textarea)
	email = forms.EmailField(label="Votre adresse mail")
