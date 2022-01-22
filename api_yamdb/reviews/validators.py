import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


def current_year():
    return datetime.date.today().year


def max_value_year(value):
    return MaxValueValidator(current_year())(value)


def range_year_validate(value):
    return MinValueValidator(-37000)(value) and max_value_year(value)
    # https://ru.wikipedia.org/wiki/%D0%93%D0%B5%D1%80%D0%BE%D0%B8%D0%B4%D1%8B
    # Героиды, год выхода: 5 год до нашей эры (или -5 год)
    # https://ria.ru/20120514/649286596.html
    # Археологи обнаружили в одной из пещер на юге Франции наскальные рисунки,
    # чей возраст оценивается в 37 тысяч лет
