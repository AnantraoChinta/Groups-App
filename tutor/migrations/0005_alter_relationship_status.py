# Generated by Django 4.1 on 2023-09-29 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tutor", "0004_alter_relationship_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="relationship",
            name="status",
            field=models.CharField(
                choices=[("accepted", "accepted"), ("sent", "sent")], max_length=8
            ),
        ),
    ]
