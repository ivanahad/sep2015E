from django import forms
from staff.models import Messages

class MessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = '__all__'
        prefix = 'message_form'
