from fastapi import FastAPI, HTTPException
from datetime import datetime
from typing import Dict
from zoneinfo import ZoneInfo
import pytz

app = FastAPI(
    title="Test Backend API",
    description="Простое тестовое API для получения текущей даты и времени сервера",
    version="1.0.0"
)


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


# Словарь для маппинга популярных названий городов к IANA часовым поясам
TIMEZONE_MAPPING = {
    "ekaterinburg": "Asia/Yekaterinburg",
    "yekaterinburg": "Asia/Yekaterinburg",
    "moscow": "Europe/Moscow",
    "saint petersburg": "Europe/Moscow",
    "petersburg": "Europe/Moscow",
    "spb": "Europe/Moscow",
    "kiev": "Europe/Kiev",
    "kyiv": "Europe/Kiev",
    "london": "Europe/London",
    "paris": "Europe/Paris",
    "berlin": "Europe/Berlin",
    "new york": "America/New_York",
    "los angeles": "America/Los_Angeles",
    "tokyo": "Asia/Tokyo",
    "beijing": "Asia/Shanghai",
    "shanghai": "Asia/Shanghai",
}


def parse_time_string(time_str: str) -> datetime:
    """
    Парсит строку времени в разных форматах и возвращает datetime в UTC
    """
    time_str = time_str.strip()
    
    # Пробуем разные форматы
    formats = [
        "%H:%M:%S",      # 15:00:00
        "%H:%M",         # 15:00
        "%Y-%m-%d %H:%M:%S",  # 2024-01-15 15:00:00
        "%Y-%m-%d %H:%M",     # 2024-01-15 15:00
        "%Y-%m-%dT%H:%M:%S",  # 2024-01-15T15:00:00
        "%Y-%m-%dT%H:%M",     # 2024-01-15T15:00
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(time_str, fmt)
            # Если указано только время, используем сегодняшнюю дату
            if "%Y" not in fmt:
                today = datetime.now(ZoneInfo("UTC")).date()
                dt = datetime.combine(today, dt.time())
            # Предполагаем, что входное время в UTC
            return dt.replace(tzinfo=ZoneInfo("UTC"))
        except ValueError:
            continue
    
    raise ValueError(f"Не удалось распознать формат времени: {time_str}")


def get_timezone(timezone_name: str) -> ZoneInfo:
    """
    Получает ZoneInfo объект по названию часового пояса
    """
    original_name = timezone_name.strip()
    timezone_name_lower = original_name.lower()
    
    # Проверяем маппинг городов
    if timezone_name_lower in TIMEZONE_MAPPING:
        iana_name = TIMEZONE_MAPPING[timezone_name_lower]
        try:
            return ZoneInfo(iana_name)
        except Exception:
            pass
    
    # Пробуем использовать напрямую как IANA timezone (с сохранением регистра)
    try:
        return ZoneInfo(original_name)
    except Exception:
        pass
    
    # Пробуем найти похожее название в списке IANA timezones
    for tz_name in pytz.all_timezones:
        if timezone_name_lower == tz_name.lower() or timezone_name_lower in tz_name.lower():
            try:
                return ZoneInfo(tz_name)
            except Exception:
                continue
    
    raise ValueError(f"Часовой пояс '{original_name}' не найден. Используйте названия городов (Ekaterinburg, Moscow) или IANA timezone (Asia/Yekaterinburg, Europe/Moscow)")


@app.get("/convert-time")
async def convert_time(
    time: str,
    timezone: str
) -> Dict[str, str]:
    """
    Конвертирует время из UTC в указанный часовой пояс
    
    Параметры:
    - time: Время в UTC (форматы: "15:00", "15:00:00", "2024-01-15 15:00:00")
    - timezone: Название часового пояса (например: "Ekaterinburg", "Asia/Yekaterinburg", "Europe/Moscow")
    
    Пример: /convert-time?time=15:00&timezone=Ekaterinburg
    Результат: 20:00 (UTC+5 для Екатеринбурга)
    """
    try:
        # Парсим входное время (предполагаем UTC)
        utc_time = parse_time_string(time)
        
        # Получаем целевой часовой пояс
        target_tz = get_timezone(timezone)
        
        # Конвертируем из UTC в целевой часовой пояс
        converted_time = utc_time.astimezone(target_tz)
        
        return {
            "input_time_utc": utc_time.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "input_time": time,
            "target_timezone": str(target_tz),
            "converted_time": converted_time.strftime("%Y-%m-%d %H:%M:%S"),
            "converted_time_only": converted_time.strftime("%H:%M:%S"),
            "time_only": converted_time.strftime("%H:%M"),
            "offset": converted_time.strftime("%z"),
            "timezone_name": str(target_tz)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка конвертации: {str(e)}")


@app.get("/timezones")
async def list_timezones() -> Dict[str, list]:
    """
    Возвращает список доступных часовых поясов (города из маппинга)
    """
    return {
        "supported_cities": list(TIMEZONE_MAPPING.keys()),
        "example_iana_timezones": [
            "Asia/Yekaterinburg",
            "Europe/Moscow",
            "Europe/Kiev",
            "America/New_York",
            "Europe/London",
            "Asia/Tokyo"
        ],
        "note": "Можно использовать как названия городов, так и IANA timezone названия"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
