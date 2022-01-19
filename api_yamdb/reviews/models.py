from django.contrib.auth import get_user_model
from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


User = get_user_model()

SCORES = [
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5),
    ('6', 6),
    ('7', 7),
    ('8', 8),
    ('9', 9),
    ('10', 10),
]


class Review(models.Model):
    text = models.TextField(max_length=500)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.SmallIntegerField(choices=SCORES)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)


class Categorie(models.Model):
    name = models.TextField('Название категории', max_length=256)
    slug = models.SlugField(
        'Адрес категории',
        unique=True,
        blank=True,
        null=True,
        max_length=50,)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.TextField('Название жанра', max_length=256)
    slug = models.SlugField('Адрес жанра', unique=True, max_length=50)

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
