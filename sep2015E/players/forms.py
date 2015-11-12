from django import forms
from players.models import User, UserRegistration, Pair

class PlayerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):    #"""When editing player informations."""
       player_id = kwargs.pop('player_id', None)
       player_email = kwargs.pop('player_email', None)
       player = None
       if player_id != None:
           player = User.objects.filter(id=player_id).get()
       if player_email != None:
           player = User.objects.filter(email=player_email).get()
       super(PlayerForm, self).__init__(*args, **kwargs)
       if player != None:
           self.fields['firstname'].initial = player.firstname
           self.fields['lastname'].initial = player.lastname
           self.fields['gender'].initial = player.gender
           self.fields['birthdate'].initial = player.birthdate
           self.fields['address_street'].initial = player.address_street
           self.fields['address_number'].initial = player.address_number
           self.fields['address_box'].initial = player.address_box
           self.fields['city'].initial = player.city
           self.fields['country'].initial = player.country
           self.fields['zipcode'].initial = player.zipcode
           self.fields['email'].initial = player.email
           self.fields['phone'].initial = player.phone

    class Meta:
        model = User
        fields = '__all__'

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = UserRegistration
        fields = [
                'level',
                'bbq',
            ]

class PairRegistrationForm(forms.ModelForm):
    class Meta:
        model = Pair
        fields = [
                'payment_method',
                'comment'
            ]
        widgets = {
                'comment': forms.Textarea(attrs={'cols': 40, 'rows': 3}),
            }

class EmailOldUserForm(forms.Form):
    """Form to recognize previous participant based on their email."""
    email = forms.EmailField(label="Email du joueur")
