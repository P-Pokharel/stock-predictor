# Generated by Django 5.1.3 on 2024-12-04 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('predictor', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockdata',
            name='volume',
            field=models.FloatField(),
        ),
    ]
