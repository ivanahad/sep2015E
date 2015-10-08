from django.shortcuts import render
from datetime import datetime
from staff.models import Messages

name = "Eric Duvoie" #replace by a call to database


def home(request):
    """Home page for staff members."""
    messages = Messages.objects.all() #replace by a call destined to the current staff member
    info = {'name': name, 'date':datetime.now(), 'messages':messages}
    return render(request, 'staff/home.html', info)
