from django.shortcuts import render
from datetime import datetime
from staff.models import Messages
from staff.forms import MessageForm
from courts.models import Court


name = "Eric Duvoie" #replace by a call to database


def home(request):
    """Home page for staff members."""

    if request.method == 'POST':

        form_msg = MessageForm(request.POST, prefix="msg")
        if form_msg.is_valid():
            Messages(author = name, \
                    destinator = form_msg.cleaned_data['destinator'], \
                    title = form_msg.cleaned_data['title'], \
                    message = form_msg.cleaned_data['message']).save()



    form_msg = MessageForm(prefix="msg")
    messages = Messages.objects.all() #replace by a call destined to the current staff member

    return render(request, 'staff/home.html', {\
            'name': name, \
            'date':datetime.now(), \
            'messages':messages, \
            'form_msg': form_msg,
            })

def courts(request):
    courts = Court.objects.all()

    return render(request, 'staff/courts.html', locals())
