# Generated by Django 4.2.5 on 2023-11-04 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator_api', '0006_datasetconfiguration_attribute_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulatordetail',
            name='producer_type',
            field=models.CharField(choices=[('kafka', 'kafka'), ('folder', 'folder')], max_length=20),
        ),
        migrations.AlterField(
            model_name='simulatordetail',
            name='sink_name',
            field=models.CharField(default='./Task1/sample_datasets/', max_length=255),
        ),
    ]