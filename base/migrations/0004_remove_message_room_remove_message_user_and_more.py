# Generated by Django 4.1 on 2023-03-26 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0003_alter_room_host"),
    ]

    operations = [
        migrations.RemoveField(model_name="message", name="room",),
        migrations.RemoveField(model_name="message", name="user",),
        migrations.RemoveField(model_name="room", name="host",),
        migrations.RemoveField(model_name="room", name="participants",),
        migrations.DeleteModel(name="Topic",),
        migrations.DeleteModel(name="Message",),
        migrations.DeleteModel(name="Room",),
    ]
