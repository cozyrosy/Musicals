# Generated by Django 4.0.6 on 2022-08-13 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0008_alter_cartitem_is_active_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
