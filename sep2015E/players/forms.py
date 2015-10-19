from django import forms
from players.models import User, UserRegistration, PAYMENT_METHODS

class PlayerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = UserRegistration
        fields = [
                'level',
                'payment_method',
                'bbq',
                'activities',
                'comment'
            ]
        widgets = {
                'comment': forms.Textarea(attrs={'cols': 40, 'rows': 3}),
                'activities': forms.Textarea(attrs={'cols':40, 'rows': 3})
            }
