# Generated by Django 4.0.6 on 2022-08-01 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_remove_category_category_img_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='image',
        ),
        migrations.RemoveField(
            model_name='category',
            name='meta_description',
        ),
        migrations.RemoveField(
            model_name='category',
            name='meta_keywords',
        ),
        migrations.RemoveField(
            model_name='category',
            name='meta_title',
        ),
        migrations.RemoveField(
            model_name='category',
            name='name',
        ),
        migrations.RemoveField(
            model_name='category',
            name='status',
        ),
        migrations.RemoveField(
            model_name='category',
            name='trending',
        ),
        migrations.AddField(
            model_name='category',
            name='cat_image',
            field=models.ImageField(blank=True, upload_to='photos/categories'),
        ),
        migrations.AddField(
            model_name='category',
            name='category_name',
            field=models.CharField(default='default', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, default='default', max_length=255),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.CharField(default='default', max_length=50, unique=True),
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
