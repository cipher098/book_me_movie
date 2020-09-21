# Generated by Django 3.0.10 on 2020-09-21 03:09

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0002_auto_20200920_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='ticket_ids',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='movie',
            name='release_date',
            field=models.DateField(default=datetime.date(2020, 9, 21), verbose_name='Movie Release Date'),
        ),
        migrations.AlterField(
            model_name='show',
            name='base_price',
            field=models.FloatField(verbose_name='Base Price'),
        ),
    ]
