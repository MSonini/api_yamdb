# Generated by Django 2.2.16 on 2022-01-20 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_auto_20220120_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.SmallIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], max_length=2),
        ),
    ]
