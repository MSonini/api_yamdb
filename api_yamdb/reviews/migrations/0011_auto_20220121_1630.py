# Generated by Django 2.2.16 on 2022-01-21 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0010_title_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(unique=True, verbose_name='Адрес жанра'),
        ),
    ]