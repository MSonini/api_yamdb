import datetime

from django.core.validators import MaxValueValidator
from django.db import models


class Categorie(models.Model):
    name = models.TextField(max_length=200)
    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.TextField(max_length=200)
    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


def current_year():
    return datetime.date.today().year


def max_value_year(value):
    return MaxValueValidator(current_year() + 10)(value)


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        blank=True
    )
    year = models.IntegerField(
        validators=[
            MaxValueValidator(current_year())
        ],
        null=True,
        db_index=True
    )
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(Genre, blank=True)
    category = models.ForeignKey(
        Categorie,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles'
    )

    def __str__(self):
        return self.name[:100]
