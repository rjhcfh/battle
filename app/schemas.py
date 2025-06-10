from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Participant(BaseModel):
    """Схема участника битвы"""
    name: str = Field(..., description="Имя участника", min_length=1, max_length=100)
    power: int = Field(..., description="Сила участника", ge=0, le=1000)

class BattleRequest(BaseModel):
    """Схема запроса на создание битвы"""
    participant1: Participant = Field(..., description="Первый участник")
    participant2: Participant = Field(..., description="Второй участник")

class BattleResult(BaseModel):
    """Схема результата битвы"""
    id: str = Field(..., description="Уникальный идентификатор битвы")
    participant1: Participant = Field(..., description="Первый участник")
    participant2: Participant = Field(..., description="Второй участник")
    winner: Optional[str] = Field(None, description="Имя победителя")
    winner_power: Optional[int] = Field(None, description="Сила победителя")
    created_at: datetime = Field(..., description="Время создания битвы")
    completed: bool = Field(..., description="Завершена ли битва")

class BattleResponse(BaseModel):
    """Схема ответа с ID битвы"""
    battle_id: str = Field(..., description="Уникальный идентификатор созданной битвы")

class ServiceInfo(BaseModel):
    """Схема информации о сервисе"""
    message: str = Field(..., description="Сообщение сервиса")
    endpoints: dict = Field(..., description="Доступные эндпоинты")
    total_battles: int = Field(..., description="Общее количество битв") 