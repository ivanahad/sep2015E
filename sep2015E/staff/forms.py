from django import forms
from staff.models import Messages
from players.models import User

class MessageForm(forms.ModelForm):
    """Form when composing a message to send to other staff memebers."""
    class Meta:
        model = Messages
        fields = '__all__'
        prefix = 'message_form'
