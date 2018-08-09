from django import forms

from django.contrib.sessions.backends.db import SessionStore

from .models import EventTicket, Event, Cart 

class AddTicketsForm(forms.Form):

    eventId = None
    authenticated = False
    

    def __init__(self, *args, **kwargs):
        
        self.authenticated = kwargs.pop("authenticated")
        self.eventId = kwargs.pop("eventId")

        super(AddTicketsForm, self).__init__(*args, **kwargs)

        self.event = Event.objects.filter(id = self.eventId)[0]
        self.ticketOptions = self.event.getAvailableTarifs()

        #filter system only
        self.ticketOptions = [x for x in self.ticketOptions if not x.isSystemOnly]

        #filter AdminOnly if not logged in
        if(not self.authenticated):
            self.ticketOptions = [x for x in self.ticketOptions if not x.isAdminOnly]

        for tarif in self.ticketOptions:
                fieldname = "%s_%s" % (self.event.id, tarif.id)
                self.fields[fieldname] = forms.ChoiceField(label= "%s : %s" % (tarif.name, tarif.description), choices=[(x, x) for x in range(0, 10)])

    def clean(self):
        eventTickets = []
        cleaned_data = super(AddTicketsForm, self).clean()

        totalTickets = 0
        for tarif in self.ticketOptions:
            fieldname = "%s_%s" % (self.event.id, tarif.id)
            totalTickets += int(self.cleaned_data[fieldname])
            eventTicket = {}
            eventTicket["quantity"] = int(self.cleaned_data[fieldname])
            eventTicket["tarif"] = tarif
            eventTickets.append(eventTicket)

        if totalTickets > self.event.seatsLeft():
            raise forms.ValidationError("Désolé... Il ne reste pas suffisamment de billets pour cet événement")
        else:
            self.cleaned_data["eventTickets"] = eventTickets
    
    def save(self):
        
        s = SessionStore()
        print(s.session_key)
        if not s.session_key:
            s.create()
        
        currentCart = Cart.objects.filter(sessionKey = s.session_key)
        if(len(currentCart) >= 1):
            currentCart = currentCart[0]

        if(not currentCart):
            currentCart = Cart.objects.create(sessionKey = s.session_key)

        for eventTicket in self.cleaned_data["eventTickets"]:
            newEventTicket = EventTicket.objects.create(event=self.event, tarif=eventTicket["tarif"], quantity=eventTicket["quantity"])
            currentCart.eventTickets.add(newEventTicket)
    
    def getTarifs(self):
        for fieldname in self.fields:
            yield self[fieldname]