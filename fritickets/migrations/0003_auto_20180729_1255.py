# Generated by Django 2.0.7 on 2018-07-29 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fritickets', '0002_auto_20180728_2337'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('csscolor', models.CharField(max_length=15)),
            ],
        ),
        migrations.AddField(
            model_name='show',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='fritickets.Category'),
        ),
    ]