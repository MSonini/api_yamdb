from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


class Categorie(models.Model):
    name = models.TextField('Название категории', max_length=200)
    slug = models.SlugField('Адрес категории', unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.TextField('Название жанра', max_length=200)
    slug = models.SlugField('Адрес жанра', unique=True)

    def __str__(self):
        return self.name


def current_year():
    return datetime.date.today().year


def max_value_year(value):
    return MaxValueValidator(current_year() + 10)(value)


class Title(models.Model):
    name = models.TextField('Название произведения', max_length=5000)
    year = models.IntegerField(
        'Год издания произведения',
        blank=True,
        null=False,
        validators=[MinValueValidator(-15000), max_value_year])
    category = models.ForeignKey(
        Categorie, on_delete=models.SET_NULL,
        related_name='titles',
        blank=False, null=True,
        verbose_name='Категория', help_text='Выберите категорию произведения',
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL,
        related_name='titles',
        blank=False, null=True,
        verbose_name='Жанр', help_text='Выберите жанр произведения',
    )

    def __str__(self):
        return self.name[:100]
