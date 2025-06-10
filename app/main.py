from fastapi import FastAPI
from endpoints import router
import uvicorn

# Создаем экземпляр FastAPI приложения
app = FastAPI(
    title="Battle Service",
    description="Сервис для проведения битв между участниками",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Регистрируем роутер с эндпоинтами
app.include_router(router,prefix="/battle")

if __name__ == "__main__":
    # Запускаем сервер
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 