# Generated by Django 4.2.6 on 2023-10-31 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("lineage", "0017_invalid_source_lineage_state"),
        ("connections", "0028_connection_validated"),
    ]

    operations = [
        migrations.AlterField(
            model_name="connection",
            name="source",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="connections", to="lineage.source"
            ),
        ),
        migrations.AlterField(
            model_name="run",
            name="connection",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="runs",
                to="connections.connection",
            ),
        ),
        migrations.AlterField(
            model_name="run",
            name="source",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="runs", to="lineage.source"
            ),
        ),
    ]