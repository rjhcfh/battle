from fastapi import APIRouter, HTTPException
from app.schemas import BattleRequest, BattleResponse, BattleResult, ServiceInfo
from app.game_logic import battle_service

# Создаем роутер для API
router = APIRouter()

@router.post("/start", response_model=BattleResponse, tags=["battles"])
async def start_battle(battle_request: BattleRequest):
    """
    Начинает новую битву между двумя участниками
    
    - **participant1**: Первый участник с именем и силой
    - **participant2**: Второй участник с именем и силой
    
    Возвращает уникальный ID битвы для получения результата.
    """
    try:
        battle_id = battle_service.create_battle(
            battle_request.participant1,
            battle_request.participant2
        )
        return BattleResponse(battle_id=battle_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка создания битвы: {str(e)}")

@router.get("/{battle_id}", response_model=BattleResult, tags=["battles"])
async def get_battle_result(battle_id: str):
    """
    Возвращает результат битвы по ID
    
    - **battle_id**: Уникальный идентификатор битвы
    
    Возвращает полную информацию о битве, включая участников и победителя.
    """
    try:
        return battle_service.get_battle(battle_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Битва не найдена")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения результата: {str(e)}")

@router.get("/", response_model=ServiceInfo, tags=["info"])
async def get_service_info():
    """
    Возвращает информацию о сервисе
    
    Предоставляет общую информацию о доступных эндпоинтах и статистике сервиса.
    """
    return ServiceInfo(
        message="Battle Service API",
        endpoints={
            "start_battle": "POST /battle/start",
            "get_result": "GET /battle/{id}",
            "service_info": "GET /battle/"
        },
        total_battles=battle_service.get_battles_count()
    )

