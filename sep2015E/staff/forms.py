from django import forms
from staff.models import Messages
from players.models import User

class MessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = '__all__'
        prefix = 'message_form'

class EditPlayerForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
