# Generated by Django 4.0.4 on 2022-05-31 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook', '0174_alter_food_substitute_userspace'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpreference',
            name='space',
        ),
    ]
