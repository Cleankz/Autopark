# Generated by Django 4.1.4 on 2022-12-29 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('autopark', '0007_alter_driver_date_of_birthday'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='driver',
            name='date_of_birthday',
        ),
    ]
