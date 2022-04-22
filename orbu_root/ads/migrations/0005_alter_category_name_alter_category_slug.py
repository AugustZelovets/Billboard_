# Generated by Django 4.0.3 on 2022-04-20 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0004_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=155, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=155, unique=True),
        ),
    ]