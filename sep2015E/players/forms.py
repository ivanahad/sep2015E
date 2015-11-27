from django import forms
from players.models import User, UserRegistration, Pair

class PlayerForm(forms.ModelForm):
    """Form for registering a new player and edit it."""
    def __init__(self, *args, **kwargs):
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
        widgets = {
                'zipcode': forms.TextInput(),
            }

class RegistrationForm(forms.ModelForm):
    """Form to register a player."""
    def __init__(self, *args, **kwargs):
       user_reg_id = kwargs.pop('user_reg_id', None)
       user_reg = None
       if user_reg_id != None:
           user_reg = UserRegistration.objects.get(pk=user_reg_id)
           #player = User.objects.filter(id=player_id).get()
       super(RegistrationForm, self).__init__(*args, **kwargs)
       if user_reg != None:
           self.fields['payement_method'].initial = user_reg.payement_method
           self.fields['payement_done'].initial = user_reg.payement_done
           self.fields['bbq'].initial = user_reg.bbq
           self.fields['level'].initial = user_reg.level

    class Meta:
        model = UserRegistration
        fields = [
                'level',
                'bbq',
                'payement_method',
                'payement_done'
            ]

class PairRegistrationForm(forms.ModelForm):
    """Form to register a new pair."""
    class Meta:
        model = Pair
        fields = [
                'comment'
            ]
        widgets = {
                'comment': forms.Textarea(attrs={'cols': 40, 'rows': 3}),
            }

class EmailOldUserForm(forms.Form):
    """Form to recognize previous participant based on their email."""
    email = forms.EmailField(label="Email du joueur")