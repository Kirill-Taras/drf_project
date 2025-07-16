# DRF Project with Docker

## 📌 Суть проекта
Проект представляет собой проект на Django Rest Framework с Docker-инфраструктурой. Включает:
- Работу с базой данных PostgreSQL
- Асинхронные задачи через Celery + Redis
- Готовую конфигурацию для разработки и тестирования

## ⚙️ Основные параметры
```
Технологии:
- Python 3.11
- Django 4.2
- DRF 3.14
- PostgreSQL 13
- Redis 7
- Celery 5.3

Сервисы в Docker:
- backend:8000   - Django приложение
- db:5432       - PostgreSQL
- redis:6379    - Redis сервер
- celery_worker - Обработчик задач
- celery_beat   - Планировщик задач
```

## ⚙️ Команды для запуска
Скопируйте шаблон .env файла
```cp .env.example .env```

Заполните .env реальными значениями
```nano .env```

Сборка и запуск
```docker-compose up --build```

Для работы в фоне:
```docker-compose up -d```

Применение миграций
```docker-compose exec backend python manage.py migrate```
