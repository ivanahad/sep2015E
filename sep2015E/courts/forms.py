from django import forms
from courts.models import Court

class RegisterForm(forms.ModelForm):

    class Meta:
        model = Court
        fields = '__all__'

class OwnerCourtsForm(forms.Form):
	owner = forms.CharField(label='Owner')