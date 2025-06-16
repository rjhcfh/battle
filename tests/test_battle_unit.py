import pytest
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app
from app.schemas import BattleRequest, Participant

client = TestClient(app)

class TestServiceInfo:
    """Тесты для эндпоинта информации о сервисе"""
    
    def test_get_service_info(self, client):
        """Тест получения информации о сервисе"""
        response = client.get("/battle/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "Battle Service API"
        assert "endpoints" in data
        assert "total_battles" in data
        assert isinstance(data["total_battles"], int)

class TestBattleCreation:
    """Тесты для создания битвы"""
    
    def test_start_battle_success(self, client, valid_battle_request):
        """Тест успешного создания битвы"""
        response = client.post("/battle/start", json=valid_battle_request)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "battle_id" in data
        assert isinstance(data["battle_id"], str)
    
    def test_start_battle_invalid_data(self, client, invalid_battle_request_missing_power):
        """Тест создания битвы с невалидными данными (отсутствует power)"""
        response = client.post("/battle/start", json=invalid_battle_request_missing_power)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_start_battle_negative_power(self, client, invalid_battle_request_negative_power):
        """Тест создания битвы с отрицательным значением power"""
        response = client.post("/battle/start", json=invalid_battle_request_negative_power)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

class TestBattleResults:
    """Тесты для получения результатов битвы"""
    
    def test_get_battle_result_success(self, client, battle_id):
        """Тест успешного получения результата битвы"""
        response = client.get(f"/battle/{battle_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "participant1" in data
        assert "participant2" in data
        assert "winner" in data
        assert data["participant1"]["name"] == "Warrior1"
        assert data["participant2"]["name"] == "Warrior2"
    
    def test_get_nonexistent_battle(self, client):
        """Тест получения результата несуществующей битвы"""
        response = client.get("/battle/nonexistent-id")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "Битва не найдена" 