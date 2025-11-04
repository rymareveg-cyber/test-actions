from fastapi import FastAPI
from datetime import datetime
from typing import Dict

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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
