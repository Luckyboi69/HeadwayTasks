# Generated by Django 4.2.5 on 2023-09-13 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator_api', '0003_simulatordetail_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasetconfiguration',
            name='noise_level',
            field=models.CharField(max_length=10),
        ),
    ]
