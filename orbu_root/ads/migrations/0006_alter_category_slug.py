# Generated by Django 4.0.3 on 2022-04-20 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0005_alter_category_name_alter_category_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(auto_created=True, max_length=155, unique=True),
        ),
    ]
