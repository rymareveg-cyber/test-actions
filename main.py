from fastapi import FastAPI, Query, HTTPException
from datetime import datetime
from typing import Dict
import pytz

app = FastAPI(
    title="Test Backend API",
    description="Простое тестовое API для получения текущей даты и времени сервера",
    version="1.0.0"
)

# Маппинг популярных названий городов на часовые пояса
TIMEZONE_ALIASES = {
    "ekaterinburg": "Asia/Yekaterinburg",
    "yekaterinburg": "Asia/Yekaterinburg",
    "екатеринбург": "Asia/Yekaterinburg",
    "moscow": "Europe/Moscow",
    "москва": "Europe/Moscow",
    "new york": "America/New_York",
    "london": "Europe/London",
    "tokyo": "Asia/Tokyo",
    "beijing": "Asia/Shanghai",
    "shanghai": "Asia/Shanghai",
    "berlin": "Europe/Berlin",
    "paris": "Europe/Paris",
    "sydney": "Australia/Sydney",
}


@app.get("/")
async def root() -> Dict[str, str]:
    """
    Корневой эндпоинт с информацией об API
    """
    return {
        "message": "Test Backend API",
        "description": "Используйте /datetime для получения текущей даты и времени",
        "docs": "/docs"
    }


@app.get("/datetime")
async def get_datetime() -> Dict[str, str]:
    """
    Возвращает текущую дату и время сервера
    """
    now = datetime.now()
    return {
        "datetime": now.isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "timezone": str(now.astimezone().tzinfo)
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Эндпоинт для проверки здоровья сервиса
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/convert-time")
async def convert_time(
    time: str = Query(..., description="Время в формате HH:MM или HH:MM:SS (UTC)"),
    timezone: str = Query(..., description="Часовой пояс (например: Asia/Yekaterinburg, Europe/Moscow, America/New_York)")
) -> Dict[str, str]:
    """
    Конвертирует время из UTC в указанный часовой пояс
    
    Примеры:
    - time=15:00&timezone=Asia/Yekaterinburg -> 20:00 (UTC+5)
    - time=15:30&timezone=Europe/Moscow -> 18:30 (UTC+3)
    """
    try:
        # Парсим время
        time_parts = time.split(":")
        if len(time_parts) < 2:
            raise ValueError("Неверный формат времени")
        
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        second = int(time_parts[2]) if len(time_parts) > 2 else 0
        
        if not (0 <= hour < 24 and 0 <= minute < 60 and 0 <= second < 60):
            raise ValueError("Время вне допустимого диапазона")
        
        # Создаем datetime объект в UTC
        today = datetime.now(pytz.UTC).date()
        utc_time = pytz.UTC.localize(datetime.combine(today, datetime.min.time().replace(hour=hour, minute=minute, second=second)))
        
        # Получаем нужный часовой пояс
        timezone_lower = timezone.lower().strip()
        
        # Сначала проверяем алиасы
        if timezone_lower in TIMEZONE_ALIASES:
            timezone = TIMEZONE_ALIASES[timezone_lower]
        
        try:
            target_tz = pytz.timezone(timezone)
        except pytz.exceptions.UnknownTimeZoneError:
            # Попытка найти часовой пояс по частичному совпадению (для удобства)
            all_timezones = pytz.all_timezones
            matching_tz = [tz for tz in all_timezones if timezone_lower in tz.lower()]
            if not matching_tz:
                raise HTTPException(
                    status_code=400,
                    detail=f"Часовой пояс '{timezone}' не найден. Используйте формат 'Region/City' (например: Asia/Yekaterinburg) или название города (Ekaterinburg, Moscow)"
                )
            if len(matching_tz) > 1:
                raise HTTPException(
                    status_code=400,
                    detail=f"Найдено несколько совпадений: {', '.join(matching_tz[:5])}. Уточните часовой пояс."
                )
            target_tz = pytz.timezone(matching_tz[0])
        
        # Конвертируем время
        converted_time = utc_time.astimezone(target_tz)
        
        return {
            "input_time_utc": time,
            "input_timezone": "UTC",
            "output_time": converted_time.strftime("%H:%M:%S"),
            "output_time_short": converted_time.strftime("%H:%M"),
            "output_datetime": converted_time.isoformat(),
            "output_timezone": str(converted_time.tzinfo),
            "timezone_name": target_tz.zone,
            "utc_offset": converted_time.strftime("%z")
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Ошибка парсинга времени: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
