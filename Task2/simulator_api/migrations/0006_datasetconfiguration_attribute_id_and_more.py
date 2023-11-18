# Generated by Django 4.2.5 on 2023-11-03 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator_api', '0005_remove_simulatordetail_meta_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasetconfiguration',
            name='attribute_id',
            field=models.CharField(default='0', max_length=30),
        ),
        migrations.AddField(
            model_name='datasetconfiguration',
            name='generator_id',
            field=models.CharField(default='0', max_length=30),
        ),
        migrations.AddField(
            model_name='simulatordetail',
            name='sink_name',
            field=models.CharField(default='0', max_length=255),
        ),
    ]