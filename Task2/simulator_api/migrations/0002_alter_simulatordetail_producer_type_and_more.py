# Generated by Django 4.2.5 on 2023-09-13 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulatordetail',
            name='producer_type',
            field=models.CharField(choices=[('Kafka', 'Kafka'), ('folder', 'CSV File')], max_length=20),
        ),
        migrations.AlterUniqueTogether(
            name='datasetconfiguration',
            unique_together={('time_series', 'frequency', 'noise_level', 'trend_coefficients', 'missing_percentage', 'outlier_percentage', 'cycle_component_frequency')},
        ),
        migrations.RemoveField(
            model_name='datasetconfiguration',
            name='cycle_component_amplitude',
        ),
    ]
