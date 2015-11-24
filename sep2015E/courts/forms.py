from django import forms
from courts.models import Court

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Court
        fields = '__all__'
        exclude = ['available']
        widgets = {
                'comment_access': forms.Textarea(attrs={'cols': 35, 'rows':3}),
                'comment_desiderata': forms.Textarea(attrs={'cols': 35, 'rows':3}),
                'zipcode': forms.TextInput()
            }


class OwnerCourtsForm(forms.Form):
	owner = forms.CharField(label='Owner')
