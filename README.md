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

### `GET /convert-time`
Конвертирует время из UTC в указанный часовой пояс

**Параметры:**
- `time` (обязательный) - время в формате HH:MM или HH:MM:SS (UTC)
- `timezone` (обязательный) - часовой пояс (можно использовать название города или формат Region/City)

**Примеры:**
```
GET /convert-time?time=15:00&timezone=Ekaterinburg
GET /convert-time?time=15:00&timezone=Asia/Yekaterinburg
GET /convert-time?time=14:30&timezone=Moscow
```

**Ответ:**
```json
{
  "input_time_utc": "15:00",
  "input_timezone": "UTC",
  "output_time": "20:00:00",
  "output_time_short": "20:00",
  "output_datetime": "2024-01-15T20:00:00+05:00",
  "output_timezone": "Asia/Yekaterinburg",
  "timezone_name": "Asia/Yekaterinburg",
  "utc_offset": "+0500"
}
```

**Поддерживаемые форматы часовых поясов:**
- Название города: `Ekaterinburg`, `Moscow`, `London`, `New York`
- Стандартный формат: `Asia/Yekaterinburg`, `Europe/Moscow`, `America/New_York`

## Документация API

После запуска приложения документация доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Docker

### Сборка образа
```bash
docker build -t test-backend-api .
```

### Запуск контейнера
```bash
docker run -d -p 8000:8000 --name test-api test-backend-api
```

### Остановка контейнера
```bash
docker stop test-api
docker rm test-api
```

### Просмотр логов
```bash
docker logs test-api
```

### Интерактивный режим (для отладки)
```bash
docker run -it -p 8000:8000 test-backend-api
```
