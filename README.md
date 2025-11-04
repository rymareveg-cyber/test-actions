# Test Backend API

Простое тестовое FastAPI приложение, возвращающее текущую дату и время сервера.

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Запуск приложения

### Вариант 1: Через Python
```bash
python main.py
```

### Вариант 2: Через uvicorn напрямую
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Эндпоинты

### `GET /`
Корневой эндпоинт с информацией об API

### `GET /datetime`
Возвращает текущую дату и время сервера в формате:
```json
{
  "datetime": "2024-01-15T14:30:45.123456",
  "date": "2024-01-15",
  "time": "14:30:45",
  "timezone": "UTC+3:00"
}
```

### `GET /health`
Проверка здоровья сервиса

## Документация API

После запуска приложения документация доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
