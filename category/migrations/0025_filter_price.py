# Generated by Django 4.0.6 on 2022-09-28 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0024_alter_categoryoffer_discount_amnt_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Filter_Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(choices=[('1000 TO 10000', '1000 TO 10000'), ('10000 TO 20000', '10000 TO 20000'), ('20000 TO 30000', '20000 TO 30000'), ('30000 TO 40000', '30000 TO 40000'), ('40000 TO 50000', '40000 TO 50000')], max_length=60)),
            ],
        ),
    ]
