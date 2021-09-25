# blog_and_comments

Сайт для создания постов, их редактирования, удаления, изменения, а также комментирования этих постов.
Присутствует возможность регистрации и авторизации.

# Запуск с использованием Docker:

## Создание контейнера docker:

* ```docker build -t container_name .```

## Поднятие контейнера docker:

* ```docker-compose up -d```

# Запуск на локальной машине:

## Установка сторонних зависимостей:

* ```pip install -r requirements.txt```

## Создание миграций:

* ```python manage.py makemigrations```

## Применение миграций:

* ```python manage.py migrate```

## Запуск сервера:

* ```python manage.py runserver```
