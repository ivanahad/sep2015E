from django.shortcuts import render
from datetime import datetime
from staff.models import Messages
from staff.forms import MessageForm

name = "Eric Duvoie" #replace by a call to database


def home(request):
    """Home page for staff members."""

    if request.method == 'POST':
        form = MessageForm(request.POST, prefix="message_form")
        if form.is_valid():
            Messages(author = name, destinator = form.cleaned_data['destinator'], title = form.cleaned_data['title'],
                    message = form.cleaned_data['message']).save()        
    else:
        form = MessageForm(prefix="message_form")

    messages = Messages.objects.all() #replace by a call destined to the current staff member
    info = {'name': name, 'date':datetime.now(), 'messages':messages, 'form': form}

    return render(request, 'staff/home.html', info)
