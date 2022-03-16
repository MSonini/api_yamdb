### Описание

REST API сервис для написания отзывов на произведения.
Документация к API доступна по эндпоинту /redoc или в файле redoc.yaml(https://github.com/MSonini/api_yamdb/blob/master/api_yamdb/static/redoc.yaml).
В проекте реализована возможность с помощью API писать отзывы к различным произведения, комментировать их. Добавлять новые произведения и жанры могут только администраторы. Также реализована регистрация через отправку письма на почту пользователя и аутентификация по токену.

### Технологии:

 - Django 2.2.16
 - Django Rest Framework 3.12.4
 - Simple-JWT 4.7.2
 - Djoser 2.1.0
 - Django-filter 21.1

### Запуск проекта в Dev-режиме:
1. Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

2. Выполнить миграции:

```
python manage.py migrate
```

3. Запустить проект:

```
python manage.py runserver
```

### Авторы:

Сонин Михаил, Никита Кечаев, Виталий Генихович.
