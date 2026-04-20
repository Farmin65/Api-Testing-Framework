# REST API Testing Framework

![Python](https://img.shields.io/badge/Python%2B-blue)
![Pytest](https://img.shields.io/badge/Pytest-orange)
![Requests](https://img.shields.io/badge/Requests-green)
![Pydantic](https://img.shields.io/badge/Pydantic-purple)

Production-grade тестовый фреймворк для автоматизированного тестирования REST API. Построен на Pytest с использованием современных практик и паттернов проектирования.

## Стек технологий

| Категория | Технология | Назначение |
|-----------|------------|------------|
| Язык | Python | Основной язык разработки |
| Тестовый фреймворк | Pytest | Запуск и организация тестов |
| HTTP клиент | Requests | Выполнение HTTP запросов |
| Валидация данных | Pydantic | Контрактное тестирование и валидация схем |
| Конфигурация | Pydantic Settings | Управление настройками через .env |
| Генерация данных | Faker | Создание случайных тестовых данных |
| Отчеты | pytest-html | Генерация HTML отчетов |
| Отчеты | Allure | Расширенные Allure отчеты |
| Параллельный запуск | pytest-xdist | Распараллеливание тестов |
| CI/CD | GitHub Actions | Автоматический запуск тестов |

## Возможности

- Модульная архитектура с четким разделением ответственности
- Автоматический retry запросов с экспоненциальным backoff при сетевых ошибках
- Валидация JSON схем ответов через Pydantic модели
- Подробное логирование всех запросов и ответов
- Генерация случайных тестовых данных через Faker
- Параллельное выполнение тестов
- Генерация HTML и Allure отчетов
- Интеграция с GitHub Actions для CI/CD
- Поддержка маркеров для выборочного запуска тестов

## Структура проекта

```
api-testing-framework/
│
├── .github/workflows/          # CI/CD пайплайны
│   └── tests.yml               # GitHub Actions workflow
│
├── config/                     # Управление конфигурацией
│   ├── __init__.py
│   └── settings.py             # Pydantic Settings
│
├── core/                       # Ядро фреймворка
│   ├── __init__.py
│   ├── client.py               # HTTP клиент с retry логикой
│   ├── assertions.py           # Кастомные ассерты для API
│   └── models.py               # Pydantic модели данных
│
├── endpoints/                  # Реализация эндпоинтов API
│   ├── __init__.py
│   ├── base.py                 # Базовый класс эндпоинта
│   ├── posts.py                # Методы для /posts
│   ├── users.py                # Методы для /users
│   └── comments.py             # Методы для /comments
│
├── tests/                      # Тестовые сьюты
│   ├── __init__.py
│   ├── conftest.py             # Фикстуры Pytest
│   ├── test_posts.py           # Тесты постов
│   ├── test_users.py           # Тесты пользователей
│   ├── test_comments.py        # Тесты комментариев
│   └── test_schema_validation.py  # Валидация схем
│
├── utils/                      # Вспомогательные утилиты
│   ├── __init__.py
│   ├── data_generator.py       # Генерация тестовых данных
│   └── logger.py               # Настройка логирования
│
├── .env.example                # Шаблон переменных окружения
├── .gitignore                  # Исключения для Git
├── pytest.ini                  # Конфигурация Pytest
├── requirements.txt            # Зависимости проекта
└── README.md                   # Документация
```

## Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/Farmin65/api-testing-framework.git
cd api-testing-framework
```

### 2. Создание виртуального окружения

```bash
python -m venv venv

# Windows
venvScriptsactivate

# Linux/macOS
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка окружения

```bash
cp .env.example .env
```

При необходимости отредактируйте `.env` файл:

```env
BASE_URL=https://jsonplaceholder.typicode.com
API_TIMEOUT=60
RETRY_COUNT=5
LOG_LEVEL=INFO
```

## Запуск тестов

### Все тесты

```bash
pytest
```

### Smoke тесты (критический функционал)

```bash
pytest -m smoke
```

### Regression тесты (полный набор)

```bash
pytest -m regression
```

### Параллельный запуск

```bash
pytest -n auto
```

### Генерация HTML отчета

```bash
pytest --html=reports/report.html --self-contained-html
```

Отчет будет доступен в папке `reports/report.html`

### Генерация Allure отчета

```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## Архитектура

### Многослойная структура

| Слой | Назначение |
|------|------------|
| `tests/` | Тестовые сценарии |
| `endpoints/` | Методы API эндпоинтов |
| `core/` | HTTP клиент, ассерты, модели валидации |
| `config/` | Настройки из .env файла |

### HTTP клиент с Retry логикой

Клиент автоматически повторяет запросы при следующих условиях:
- HTTP статусы: 429, 500, 502, 503, 504
- Ошибки соединения и таймауты
- Экспоненциальный backoff с фактором 1

### Валидация контрактов

Pydantic модели гарантируют соответствие ответов API ожидаемой схеме:

```python
class Post(BaseModel):
    userId: int = Field(..., ge=1)
    id: int
    title: str
    body: str
```

## CI/CD

Проект интегрирован с GitHub Actions. Пайплайн запускается:

- При push в main/master
- При создании Pull Request

### Шаги пайплайна

1. Checkout кода
2. Установка Python 3.11
3. Установка зависимостей
4. Запуск smoke тестов
5. Генерация HTML отчета
6. Загрузка отчета как артефакта

## Тестируемый API

В качестве тестового API используется [JSONPlaceholder](https://jsonplaceholder.typicode.com) - бесплатный fake REST API для тестирования и прототипирования.

### Доступные ресурсы

| Ресурс | Методы | Описание |
|--------|--------|----------|
| /posts | GET, POST, PUT, PATCH, DELETE | Посты блога |
| /users | GET, POST, PUT, PATCH, DELETE | Пользователи |
| /comments | GET, POST, PUT, PATCH, DELETE | Комментарии к постам |

## Результаты тестирования

Актуальный статус тестов отображается в бейдже вверху страницы.

Пример вывода при запуске:

```
collected 27 items

tests/test_posts.py::TestPostsCRUD::test_get_all_posts PASSED
tests/test_posts.py::TestPostsCRUD::test_create_post PASSED
tests/test_users.py::TestUsersAPI::test_get_all_users PASSED

==================== 25 passed, 2 failed in 164.83s ====================
```

## Расширение фреймворка

### Добавление нового эндпоинта

1. Создать класс в `endpoints/`:

```python
from endpoints.base import BaseEndpoint

class NewEndpoint(BaseEndpoint):
    path = "resource-name"
```

2. Создать тестовый класс в `tests/`:

```python
class TestNewEndpoint:
    def test_get_resource(self, new_endpoint):
        response = new_endpoint.get_list()
        new_endpoint.assertions.assert_status_code(response, 200)
```

3. Добавить фикстуру в `conftest.py`:

```python
@pytest.fixture(scope="session")
def new_endpoint():
    return NewEndpoint()
```




