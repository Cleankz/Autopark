# Generated by Django 4.1.4 on 2023-01-20 06:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autopark', '0015_alter_vehicle_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='routes',
            options={'ordering': ['car'], 'verbose_name': 'Трек', 'verbose_name_plural': 'Треки'},
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 1, 20, 6, 38, 58, 254904), null=True),
        ),
        migrations.DeleteModel(
            name='GPSRoute',
        ),
    ]