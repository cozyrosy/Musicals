# Generated by Django 4.0.6 on 2022-08-13 09:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0004_alter_cartitem_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='user',
        ),
    ]
