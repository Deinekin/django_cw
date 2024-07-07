# Generated by Django 5.0.6 on 2024-07-04 18:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0002_client_owner_message_owner_alter_mailing_message_log"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="log",
            name="owner",
        ),
        migrations.AddField(
            model_name="mailing",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="владелец",
            ),
        ),
    ]
