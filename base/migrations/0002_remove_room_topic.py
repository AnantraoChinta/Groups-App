# Generated by Django 4.1 on 2023-03-18 23:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="room", name="topic",),
    ]
