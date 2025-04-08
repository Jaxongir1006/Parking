# Generated by Django 5.1.7 on 2025-04-04 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_booking_arrived_time_alter_booking_left_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('booked', 'Booked'), ('arrived', 'Arrived'), ('left', 'Left'), ('rejected', 'Rejected')], default='booked', max_length=20),
        ),
    ]
