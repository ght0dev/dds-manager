# DDS Manager

Веб-сервис для управления движением денежных средств (ДДС) компании или личных финансов.  
Позволяет вести учет поступлений и списаний с гибкой системой категорий, подкатегорий и типов транзакций.

---

## Основные возможности

- **Создание транзакций**  
  - Поля: дата, статус (Бизнес/Личное/Налог), тип (Пополнение/Списание), категория, подкатегория, сумма, комментарий.  
  - Дата заполняется автоматически, но может быть изменена вручную.  

- **Редактирование и удаление транзакций**  
- **Просмотр списка транзакций**  
  - Таблица с фильтрацией по дате, статусу, типу, категории и подкатегории.  
  - Поддержка пагинации.  

- **Управление справочниками**  
  - Статусы, типы, категории и подкатегории можно добавлять, редактировать и удалять.  
  - Подкатегории привязаны к категориям, а категории — к типам.  

- **Валидация данных**  
  - Обязательные поля: сумма, тип, категория, подкатегория.  
  - Валидация на стороне клиента и сервера.

---

## Технологии

- Python 3.12, Django, Django REST Framework  
- База данных: SQLite (по умолчанию)  
- Frontend: минимальный интерфейс через Django admin + HTML/CSS/JS (Bootstrap)  
- Асинхронные запросы и динамические фильтры через JavaScript fetch API  

---

## Установка и запуск

1. **Клонировать репозиторий**

```
git clone https://github.com/ght0dev/dds-manager.git
cd dds-manager
```

запустить uv 

```
uv sync
```

активировать окружение 
```
source .venv/bin/activate
```

python manage.py migrate
Создать суперпользователя (для админки)

python manage.py createsuperuser
Запустить сервер

python manage.py runserver
Открыть приложение
Перейти в браузере по адресу: http://127.0.0.1:8000/

Структура проекта
```
├── project
│   ├── api
│   │   ├── __init__.py
│   │   └── urls.py
│   ├── core
│   │   ├── asgi.py
│   │   ├── __init__.py
│   │   ├── settings
│   │   │   ├── base.py
│   │   │   └── dev.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── fixtures
│   │   └── seed.json
│   ├── manage.py
│   ├── static
│   │   └── js
│   │       ├── form.js
│   │       └── transactions.js
│   ├── templates
│   │   └── transactions
│   │       ├── form.html
│   │       └── list.html
│   └── transactions
│       ├── admin.py
│       ├── apps.py
│       ├── filters.py
│       ├── __init__.py
│       ├── models.py
│       ├── serializers.py
│       ├── tests.py
│       ├── urls.py
│       └── views.py
├── pyproject.toml
├── README.md
└── uv.lock
```
API Endpoints (DRF)
```
Endpoint	Method	Описание
/api/transactions/	GET	Список транзакций с пагинацией
/api/transactions/	POST	Создание транзакции
/api/transactions/<id>/	GET	Получить транзакцию
/api/transactions/<id>/	PUT	Редактировать транзакцию
/api/transactions/<id>/	DELETE	Удалить транзакцию
/api/types/	GET	Список типов
/api/categories/	GET	Список категорий (фильтр по типу)
/api/subcategories/	GET	Список подкатегорий (фильтр по категории)
/api/statuses/	GET	Список статусов
```
Лицензия
MIT License © 2025
