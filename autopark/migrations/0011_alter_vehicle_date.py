# Generated by Django 4.1.4 on 2023-01-10 16:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autopark', '0010_enterprise_zoner_alter_vehicle_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 10, 16, 17, 23, 284186)),
        ),
    ]
