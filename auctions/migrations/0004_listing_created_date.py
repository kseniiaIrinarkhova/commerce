# Generated by Django 4.2.2 on 2023-08-10 03:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_bid_delete_bit'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]