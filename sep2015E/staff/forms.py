from django import forms
from staff.models import Messages, Files
from players.models import User

class MessageForm(forms.ModelForm):
    """Form when composing a message to send to other staff memebers."""
    class Meta:
        model = Messages
        exclude = ['author']
        widgets = {
                'message': forms.Textarea(attrs={'cols': 30, 'rows': 5}),
            }
        prefix = 'message_form'

class MailListForm(forms.Form):
    """Form for sending mass emails to all users in the database."""
    subject = forms.CharField(label='Sujet', min_length=1, max_length=64)
    content = forms.CharField(label='Contenu du message',
            widget=forms.Textarea(attrs={'cols':40, 'rows':5}))


class FilesForm(forms.ModelForm):
    """ Form for staff to upload a file """
    class Meta:
        model = Files
        exclude = ['owner']
        prefix = 'files_form'
