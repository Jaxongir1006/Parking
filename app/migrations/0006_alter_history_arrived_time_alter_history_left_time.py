# Generated by Django 5.1.7 on 2025-04-10 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_history'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='arrived_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='history',
            name='left_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
