# Generated by Django 2.2.16 on 2022-01-19 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20220119_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(help_text='Выберите категорию произведения', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='c_titles', to='reviews.Categorie', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(blank=True, related_name='g_titles', to='reviews.Genre', verbose_name='Жанры'),
        ),
    ]