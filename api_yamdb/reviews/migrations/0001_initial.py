# Generated by Django 2.2.16 on 2022-01-19 18:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import reviews.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=256, verbose_name='Название категории')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Адрес категории')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=200)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=256, verbose_name='Название жанра')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Адрес жанра')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500)),
                ('score', models.SmallIntegerField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10)])),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=200, verbose_name='Название произведения')),
                ('description', models.TextField(blank=True, verbose_name='Описание произведения')),
                ('year', models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(-15000), reviews.validators.max_value_year], verbose_name='Год издания произведения')),
                ('category', models.ForeignKey(help_text='Выберите категорию произведения', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='c_titles', to='reviews.Categorie', verbose_name='Категория')),
                ('genre', models.ManyToManyField(blank=True, related_name='g_titles', to='reviews.Genre', verbose_name='Жанры')),
            ],
        ),
    ]
