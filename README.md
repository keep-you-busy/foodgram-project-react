# Проект «Продуктовый помощник»
Проект "Продуктовый помощник" создан с целью предоставления платформы для публикации рецептов. Этот веб-сайт позволит пользователям делиться своими кулинарными рецептами, сохранять рецепты других авторов в избранное и подписываться на обновления от других участников. Сервис "Список покупок" обеспечит возможность создавать списки продуктов, необходимых для приготовления выбранных блюд.
-- -
## Сайт доступен по адресу: http://foodgram-project.zapto.org/
-- -
### Для запуска приложения в контейнерах:
- Установите Docker
- Клонируйте репозиторий
``` git clone git@github.com:keep-you-busy/foodgram-project-react.git ```
- Создайте и заполните файл .env
-- -
### Заполнение .env файла:
- POSTGRES_USER=django_user
- POSTGRES_PASSWORD=mysecretpassword
- POSTGRES_DB=django
- DB_HOST=localhost
- DB_PORT=5432
- ALLOWED_HOSTS=,127.0.0.1,localhost
- SECRET_KEY=django_secret_key
- DEBUG=True
-- -
- Запустите docker-compose
``` sudo docker-compose up -d --build ```
- Выполните миграции
``` sudo docker-compose exec backend python manage.py migrate ```
- Для сбора статики воспользуйтесь командами
``` sudo docker-compose exec backend python manage.py collectstatic --no-input ```
``` sudo docker compose exec backend cp -r /app/collected_static/. /backend_static/static/ ``` 
- Для загрузки базы данных ингрединтов
``` sudo docker-compose exec backend python manage.py loadcsvdata ```
- Для создания суперпользователя
``` sudo docker-compose exec backend python manage.py createcustomsuperuser ```
-- -
### Для доступа в админ-зону:
https://foodgram-project.zapto.org/admin/
- Логин: admin@admin.com
- Пароль: admin
-- -
### Технологии:
- Python
- Postgres
- Django Rest Framework
- Docker
- Nginx
-- -
### Автор:
[keepyoubusy](https://github.com/keep-you-busy)