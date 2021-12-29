# api_yamdb
api_yamdb
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/MSonini/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
For Unix: python3 -m venv env
for Win: python -m venv venv
```

```
For Unix: source env/bin/activate
for Win: PS: venv/scripts/activate
    OR cmd: /venv/Scripts/activate.bat
```

```
For Unix: python3 -m pip install --upgrade pip
for Win: python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
For Unix: pip install -r requirements.txt
for Win: pip install -r requirements.txt
```

Выполнить миграции:

```
For Unix: python3 manage.py migrate
for Win: python manage.py migrate
```

Запустить проект:

```
For Unix: python3 manage.py runserver
for Win: python manage.py runserver
```
