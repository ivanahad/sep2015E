from django.shortcuts import render
from datetime import datetime


name = "Eric Duvoie" #replace by a call to database

def home(request):
    """Home page for staff members."""
    return render(request, 'staff/home.html')
