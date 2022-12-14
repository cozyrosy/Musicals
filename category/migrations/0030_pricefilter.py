# Generated by Django 4.0.6 on 2022-09-28 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0029_delete_pricefilter'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(blank=True, choices=[('1000 TO 10000', '1000 TO 10000'), ('10000 TO 20000', '10000 TO 20000'), ('20000 TO 30000', '20000 TO 30000'), ('30000 TO 40000', '30000 TO 40000'), ('40000 TO 50000', '40000 TO 50000')], default='11000 TO 10000', max_length=60, null=True)),
            ],
        ),
    ]
