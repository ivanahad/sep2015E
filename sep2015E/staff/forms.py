from django import forms
from staff.models import Messages, Files, Staff
from players.models import User
from courts.models import Court
from django.contrib.auth.models import User as Django_User

class StaffEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       user_id = kwargs.pop('user_id', None)
       staff = None
       if user_id != None:
           staff = Staff.objects.filter(user__pk=user_id)
       super(StaffEditForm, self).__init__(*args, **kwargs)
       if user_id != None and staff.count() == 1:
           staff = staff.get()
           self.fields['address'].initial = staff.address
           self.fields['city'].initial = staff.city
           self.fields['country'].initial = staff.country
           self.fields['zipcode'].initial = staff.zipcode
           self.fields['phone'].initial = staff.phone
    class Meta:
        model = Staff
        exclude = ['user']
        widgets = {
                'zipcode': forms.TextInput(),
            }

class UserDjangoEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       user_id = kwargs.pop('user_id', None)
       user = None
       if user_id != None:
           user = Django_User.objects.get(pk=user_id)
       super(UserDjangoEditForm, self).__init__(*args, **kwargs)
       if user != None:
           self.fields['username'].initial = user.username
           self.fields['first_name'].initial = user.first_name
           self.fields['last_name'].initial = user.last_name
           #self.fields['email'].initial = user.email
           #self.fields['password'].initial = user.password
    class Meta:
        model = Django_User
        fields = ['username', 'first_name', 'last_name']#, 'email', 'password']

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

class SearchForm(forms.Form):
    """ Form for staff to use the search fonctionnality """
    GENDER_LIST= (("A", "Mixte"), ("M", "Homme"), ("F", "Femme"))
    BIRTHDATE_EQUALITY_LIST = ((">", "plus grand que"), ("<", "plus petit que"), ("=", "égal"))
    PAIR_LIST=(("T", "en pair"), ("F", "solo"), ("A", "----"))
    TOURNAMENT_LIST=(("T", "dans un tournoi"), ("F", "dans aucun tournoi"), ("A", "----"))
    name = forms.CharField(max_length=64, required=False)
    gender = forms.ChoiceField(choices=GENDER_LIST)
    birthdate_equality = forms.ChoiceField(choices=BIRTHDATE_EQUALITY_LIST)
    birthdate = forms.DateField(required=False)
    in_pair = forms.ChoiceField(choices=PAIR_LIST)
    in_tournament = forms.ChoiceField(choices=TOURNAMENT_LIST)

class EditCourtForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       id_court = kwargs.pop('id_court', None)
       court = Court.objects.get(pk=id_court)
       super(EditCourtForm, self).__init__(*args, **kwargs)
       if court != None:
           self.fields['owner_firstname'].initial = court.owner_firstname
           self.fields['owner_lastname'].initial = court.owner_lastname
           self.fields['owner_address_street'].initial = court.owner_address_street
           self.fields['owner_address_number'].initial = court.owner_address_number
           self.fields['owner_address_box'].initial = court.owner_address_box
           self.fields['city'].initial = court.city
           self.fields['zipcode'].initial = court.zipcode
           self.fields['email'].initial = court.email
           self.fields['phone'].initial = court.phone

           self.fields['address_street'].initial = court.address_street
           self.fields['address_number'].initial = court.address_number
           self.fields['address_box'].initial = court.address_box
           self.fields['ground'].initial = court.ground
           self.fields['cover'].initial = court.cover
           self.fields['image'].initial = court.image
           self.fields['comment_access'].initial = court.comment_access
           self.fields['comment_desiderata'].initial = court.comment_desiderata
           self.fields['available'].initial = court.available

    class Meta:
        model = Court
        exclude = ['log']
        widgets = {
                'zipcode': forms.TextInput(),
            }
