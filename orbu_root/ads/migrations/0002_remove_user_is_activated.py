# Generated by Django 4.0.3 on 2022-04-16 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_activated',
        ),
    ]