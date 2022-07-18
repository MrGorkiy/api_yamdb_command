# api_yamdb

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

# Техническая документация проекта api_yamdb
Документация API YaMDb доступна по адресу: http://127.0.0.1:8000/redoc/


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
```bash
docker pull mrgorkiy/infra:v1.0
```
```bash
git clone git@github.com:MrGorkiy/api_yamdb.git

cd api_yamdb
```

Выполнить миграции:

```bash
docker-compose exec web python manage.py migrate
```

Создать суперпользователя:

```bash
docker-compose exec web python manage.py createsuperuser
```

Шаблон наполнения env-файла
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
```

Для запуска приложения в контейнерах используйте команду
```bash
 docker-compose up -d --build

```

Заполнение БД
```bash
python manage.py shell  
# выполнить в открывшемся терминале:
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> quit()

python manage.py loaddata fixtures.json
```

# Технологии
```
Python, Django, HTTP, Django Rest Framework, SQLite3
```

# Авторы

- Брысин Максим (mbrysin95@yandex.ru)