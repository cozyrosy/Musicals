# Generated by Django 4.0.6 on 2022-07-29 05:35

import category.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='category_img',
        ),
        migrations.RemoveField(
            model_name='category',
            name='category_name',
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, default='DEFAULT VALUE', null=True, upload_to=category.models.get_file_path),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_description',
            field=models.TextField(default='DEFAULT VALUE', max_length=500),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_keywords',
            field=models.CharField(default='DEFAULT VALUE', max_length=150),
        ),
        migrations.AddField(
            model_name='category',
            name='meta_title',
            field=models.CharField(default='DEFAULT VALUE', max_length=150),
        ),
        migrations.AddField(
            model_name='category',
            name='name',
            field=models.CharField(default='DEFAULT VALUE', max_length=150),
        ),
        migrations.AddField(
            model_name='category',
            name='status',
            field=models.BooleanField(default=False, help_text='0=default, 1-Hidden'),
        ),
        migrations.AddField(
            model_name='category',
            name='trending',
            field=models.BooleanField(default=False, help_text='0=default, 1-Trending'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(default='DEFAULT VALUE', max_length=500),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.CharField(max_length=150),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=150)),
                ('name', models.CharField(default='DEFAULT VALUE', max_length=150)),
                ('product_image', models.ImageField(blank=True, default='DEFAULT VALUE', null=True, upload_to=category.models.get_file_path)),
                ('small_description', models.TextField(default='DEFAULT VALUE', max_length=250)),
                ('quantity', models.IntegerField(default='DEFAULT VALUE')),
                ('description', models.TextField(default='DEFAULT VALUE', max_length=500)),
                ('original_price', models.FloatField(default='DEFAULT VALUE')),
                ('selling_price', models.FloatField(default='DEFAULT VALUE')),
                ('status', models.BooleanField(default=False, help_text='0=default, 1-Hidden')),
                ('trending', models.BooleanField(default=False, help_text='0=default, 1-Trending')),
                ('tag', models.CharField(default='DEFAULT VALUE', max_length=150)),
                ('meta_title', models.CharField(default='DEFAULT VALUE', max_length=150)),
                ('meta_keywords', models.CharField(default='DEFAULT VALUE', max_length=150)),
                ('meta_description', models.TextField(default='DEFAULT VALUE', max_length=500)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
            ],
        ),
    ]
