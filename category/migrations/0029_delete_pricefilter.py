# Generated by Django 4.0.6 on 2022-09-28 02:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0028_alter_pricefilter_price'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PriceFilter',
        ),
    ]
