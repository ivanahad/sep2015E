from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
 
def index(request):
    return render_to_response('home/index.html', context_instance=RequestContext(request))

def sponsors(request):
    return render_to_response('home/sponsors.html', context_instance=RequestContext(request))

def contact(request):
    return render_to_response('home/contact.html', context_instance=RequestContext(request))
