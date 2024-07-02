# Generated by Django 4.2.13 on 2024-06-06 01:27

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(default={'number': 'invalid'}, max_length=128, region=None),
        ),
    ]
