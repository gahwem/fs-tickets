from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Event, EventBundle
from django.template import loader
import datetime
from .forms import AddTicketsForm

# Create your views here.

def index(request):
    all_events = Event.objects.order_by('-schedule')
    context = {
        'all_events' : all_events,
    }
    return render(request, 'fritickets/index.html', context) 



def events(request):

    if not request.session.exists(request.session.session_key):
        request.session.create() 
    
    request.session.modified = True

    bundles = EventBundle.objects.all()
    eventCalendar = Event.dates.all()

    context = {
        'bundles' : bundles,
        'eventCalendar' : eventCalendar
    }
    return render(request, 'fritickets/events.html', context) 


def eventDetail(request, eventId):
    
    if request.method == "POST":
        form = AddTicketsForm(request.POST, eventId = eventId, authenticated = request.user.is_authenticated)
        if form.is_valid():
            form.save()
            return redirect('events')

    else:
        form = AddTicketsForm(eventId = eventId, authenticated = request.user.is_authenticated)
    
    
    return render(request, 'fritickets/eventDetail.html', {'form':form})