# Generated by Django 4.2.5 on 2023-09-13 01:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simulator_api', '0004_alter_datasetconfiguration_noise_level'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='simulatordetail',
            name='meta_data',
        ),
    ]
