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
Конвертирует время из UTC в указанный часовой пояс.

**Параметры:**
- `time` (строка) - Время в UTC. Поддерживаемые форматы:
  - `15:00` или `15:00:00` - только время
  - `2024-01-15 15:00:00` - дата и время
  - `2024-01-15T15:00:00` - ISO формат
- `timezone` (строка) - Название часового пояса или города:
  - Названия городов: `Ekaterinburg`, `Moscow`, `London`, `New York`, `Tokyo` и др.
  - IANA timezone: `Asia/Yekaterinburg`, `Europe/Moscow`, `Europe/London` и др.

**Пример запроса:**
```
GET /convert-time?time=15:00&timezone=Ekaterinburg
```

**Пример ответа:**
```json
{
  "input_time_utc": "2024-01-15 15:00:00 UTC",
  "input_time": "15:00",
  "target_timezone": "Asia/Yekaterinburg",
  "converted_time": "2024-01-15 20:00:00",
  "converted_time_only": "20:00:00",
  "time_only": "20:00",
  "offset": "+0500",
  "timezone_name": "Asia/Yekaterinburg"
}
```

### `GET /timezones`
Возвращает список поддерживаемых городов и примеры IANA timezone названий

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
