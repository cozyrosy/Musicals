# Generated by Django 4.0.6 on 2022-09-28 03:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0031_alter_pricefilter_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='filter_pricee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='category.pricefilter'),
        ),
    ]
