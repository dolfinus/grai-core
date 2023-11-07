# Generated by Django 4.1.7 on 2023-02-24 11:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("django_celery_beat", "0016_alter_crontabschedule_timezone"),
        ("connections", "0013_alter_connector_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="connection",
            name="task",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="connections",
                to="django_celery_beat.periodictask",
            ),
        ),
    ]