# Generated by Django 2.0.7 on 2018-08-06 20:02

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('fritickets', '0005_eventbundle'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EventTickets',
            new_name='EventTicket',
        ),
    ]
