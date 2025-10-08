# GitHub Actions + FastAPI Project

Проект на **FastAPI** с автоматизацией через **GitHub Actions**: тесты, сборка, вёрстка.  
Цель — показать CI-конвейер для backend-приложения.

```

## 📂 Структура проекта
├── .github/
│ └── workflows/
│ └── ci.yml # workflow CI (тесты, сборка)
│
├── app/ # Исходный код приложения
│ ├── api/ # Эндпоинты / роутеры
│ ├── core/ # Конфигурации, утилиты
│ ├── db/ # Модели, подключение к БД
│ ├── schemas/ # Pydantic-схемы
│ └── main.py # Точка входа (FastAPI app)
│
├── tests/ # Тесты pytest
│
├── Dockerfile # Docker-образ приложения
├── docker-compose.yml # (опционально) конфигурация docker-compose
├── requirements.txt # Зависимости Python
├── .env.example # Пример переменных окружения
└── README.md #

```

## 🧾 Что реализовано

- API-эндпоинты (CRUD или базовый набор)  
- Валидация данных через Pydantic  
- Тесты через pytest  
- Dockerfile — контейнеризация приложения  
- CI workflow через GitHub Actions: запуск тестов, проверка кода, сборка  

```

## 🚀 Как запустить локально

1. Клонируй репозиторий  
   ```bash
   git clone https://github.com/sanek671/github-actions-fastapi.git
   cd github-actions-fastapi

Создай .env (или используй .env.example) с нужными параметрами, например:
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/dbname
(Опционально) Запусти через Docker Compose:
docker-compose up --build
Или запусти напрямую:
pip install -r requirements.txt
uvicorn app.main:app --reload
Приложение будет доступно по адресу http://localhost:8000.

🧪 Тестирование
pytest -v
Тесты находятся в папке tests/.

✅ GitHub Actions / CI

В .github/workflows/ci.yml настроен workflow, который:
запускается при push / pull_request
устанавливает Python
устанавливает зависимости
прогоняет тесты
при успешности — optional: билд Docker-образа, линтинг и другие проверки

📘 Документация API
После запуска приложения доступны:
Swagger UI → http://localhost:8000/docs
ReDoc → http://localhost:8000/redoc
