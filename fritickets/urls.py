from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('events', views.events, name='events'),
    path('detail/<int:eventId>', views.eventDetail, name="detail")
]