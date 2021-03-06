# Generated by Django 2.0.7 on 2018-07-30 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fritickets', '0004_auto_20180730_2018'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventBundle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=50)),
                ('availableTarifs', models.ManyToManyField(to='fritickets.Tarif')),
                ('events', models.ManyToManyField(to='fritickets.Event')),
            ],
        ),
    ]
