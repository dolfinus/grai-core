# Generated by Django 4.2.6 on 2023-10-27 09:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("workspaces", "0007_workspace_ai_enabled"),
    ]

    operations = [
        migrations.AddField(
            model_name="workspace",
            name="sample_data",
            field=models.BooleanField(default=False),
        ),
    ]