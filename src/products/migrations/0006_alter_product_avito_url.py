# Generated by Django 4.2.13 on 2024-06-06 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_remove_basket_avito_url_product_avito_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='avito_url',
            field=models.URLField(default=''),
        ),
    ]
