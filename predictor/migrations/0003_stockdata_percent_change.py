# Generated by Django 5.1.3 on 2024-12-07 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0002_alter_stockdata_volume'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockdata',
            name='percent_change',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
