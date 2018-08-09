from django.db import models
import datetime
from django.db.models import Sum
from django.core.exceptions import ValidationError

# Create your models here.

class Person(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=30)
    remark = models.CharField(max_length=500)

    def __str__(self):
        return self.firstname + " "  + self.lastname
 
class Category(models.Model):
    name = models.CharField(max_length=30)
    csscolor = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Tarif(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    amount = models.FloatField()
    isSystemOnly = models.BooleanField()
    isAdminOnly = models.BooleanField()

    def __str__(self):
        return self.name + " (" + self.description + ") - " + str(self.amount) + " CHF"


class Show(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.title + " - " + self.description

class DateCalendar(object):
    def __init__(self, date, events):
        self.date = date
        self.events = events

class EventDatesManager(models.Manager):

    def get_queryset(self):
        allEvents = super(EventDatesManager, self).get_queryset().all()
        allDates = list(set((e.schedule.date() for e in allEvents)))

        dates = []
        for date in allDates:
            events = [e for e in allEvents if e.schedule.date() == date]
            events.sort(key=lambda e: e.schedule)
            dc = DateCalendar(date, events)
            dates.append(dc)
        dates.sort(key=lambda dc: dc.date)
        return dates


class Event(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    location = models.CharField(max_length=30)
    schedule = models.DateTimeField()
    availableTarifs = models.ManyToManyField(Tarif)
    totalPlaces = models.IntegerField()
    objects = models.Manager()
    dates = EventDatesManager()

    def __str__(self):
        return self.show.title + " - " + str(self.schedule)

    def seatsLeft(self, excludeId = -1):
        return self.totalPlaces - (EventTicket.objects.filter(event=self.id).exclude(id=excludeId).aggregate(Sum('quantity'))['quantity__sum'] or 0)

    def getAvailableTarifs(self):
        return self.availableTarifs.all()

class EventBundle(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=50)
    events = models.ManyToManyField(Event)
    availableTarifs = models.ManyToManyField(Tarif)


class EventTicket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    tarif = models.ForeignKey(Tarif, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    validated = models.BooleanField(default=False)

    def __str__(self):
        return str(self.quantity)  + " billets tarif : " + self.tarif.name + " pour " + self.event.show.title

    def clean(self):
        super(EventTicket, self).clean()
        if(self.quantity > self.event.seatsLeft(self.id)):
            raise ValidationError('not enought seats left', code='full')

    

class Booking(models.Model):
    eventTickets = models.ManyToManyField(EventTicket)
    person =  models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return "réservations pour " + __str__(self.person)

class Cart(models.Model):
    sessionKey = models.CharField(max_length=30)
    eventTickets = models.ManyToManyField(EventTicket)

    def __str__(self):
        return "current cart for session : " + self.sessionKey

    
