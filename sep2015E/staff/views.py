from django.shortcuts import render

# Create your views here.

def home(request):
    """Welcoming page for staff members."""
    return render(request, 'staff/home.html')
