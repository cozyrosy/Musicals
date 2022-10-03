# Generated by Django 4.0.6 on 2022-09-22 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Order Confirmed', 'Order Confirmed'), ('Order Shipped', 'Order Shipped'), ('Out for delivery', 'Out for delivery'), ('Order Delivered', 'Order Delivered')], default='Order Confirmed', max_length=150),
        ),
    ]
