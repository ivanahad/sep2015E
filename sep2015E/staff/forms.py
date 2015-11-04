from django import forms
from staff.models import Messages
from players.models import User

class MessageForm(forms.ModelForm):
    """Form when composing a message to send to other staff memebers."""
    class Meta:
        model = Messages
        fields = '__all__'
        prefix = 'message_form'


class EditPlayerForm(forms.ModelForm):
    """Form when editing player informations."""
    def __init__(self, *args, **kwargs):    #Fill the fields.
       player_id = kwargs.pop('player_id')
       player = User.objects.filter(id=player_id).get()
       super(EditPlayerForm, self).__init__(*args, **kwargs)
       self.fields['firstname'].initial = player.firstname
       self.fields['lastname'].initial = player.lastname
       self.fields['address'].initial = player.address
       self.fields['city'].initial = player.city
       self.fields['country'].initial = player.country
       self.fields['zipcode'].initial = player.zipcode
       self.fields['email'].initial = player.email
       self.fields['phone'].initial = player.phone

    class Meta:
        model = User
        fields = '__all__'
