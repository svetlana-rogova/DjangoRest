# Online Learning Platform
## Описание:
Backend-приложение для онлайн-платформы обучения, разработанное с использованием Django REST Framework.  
Проект позволяет управлять курсами, уроками, подписками пользователей и платежами, а также включает асинхронную 
обработку задач с помощью Celery и Redis.
## Функционал:
- Управление пользователями (регистрация, авторизация, права доступа)
- Создание и управление курсами
- Создание уроков внутри курсов
- Система подписок на курсы
- Система платежей
- REST API на Django REST Framework
- Использование ViewSets и Generic Views
- Сериализаторы и кастомные валидаторы
- Пагинация
- Настройка прав доступа (permissions)
- Документация API (Swagger / drf-yasg)
- Асинхронные задачи (Celery)
- Интеграция платежной системы Stripe
- Настройка CORS для взаимодействия с фронтендом
- Redis как брокер сообщений и backend результатов
- Тестирование приложения
- Контейнеризация приложения с использованием Docker и Docker Compose

## Установка и использование (Docker):
1. Откройте PyCharm
2. Клонируйте репозиторий:
```
git clone https://github.com/svetlana-rogova/DjangoRest
```
3. Перейдите в папку проекта::
```
cd DjangoRest
```
4. Создайте файл `.env` из шаблона `.env.example`:

5. Запустите проект:
```
docker-compose up
```
## Структура проекта:

- materials/ — уроки, курсы и подписка на них
- users/ — пользователи и их платежи
- config/ — настройки проекта

## Тестирование:
Все тесты лежат в модуле materials/tests.py, имена функций начинаются с test_.
Запустить тесты можно через команду pytest в терминале:
```
python manage.py test
```

Проверить покрытие можно через команду:
```
coverage report
```

## Deployment

Проект развёрнут на Ubuntu Server.

Используются:
- Nginx
- Gunicorn
- PostgreSQL

## CI/CD

GitHub Actions pipeline включает:

- линт 
- тесты
- сборку Docker image 
- деплой на сервер после успешного push и pull_request

## Технологии:
- Python 3.13
- Django
- Django REST Framework
- PostgreSQL
- Celery
- Redis
- Docker / Docker Compose
- drf-yasg (Swagger)
- Stripe API