from django.contrib import admin

# Register your models here.
from .models import Show, Event, Tarif, Category, EventTicket, EventBundle

admin.site.register(Show)
admin.site.register(Event)
admin.site.register(Tarif)
admin.site.register(Category)
admin.site.register(EventTicket)
admin.site.register(EventBundle)