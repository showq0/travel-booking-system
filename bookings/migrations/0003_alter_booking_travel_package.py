# Generated by Django 5.1.5 on 2025-02-04 01:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_alter_travelpackage_available_slot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='travel_package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='bookings.travelpackage'),
        ),
    ]
