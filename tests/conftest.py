import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas import Participant

@pytest.fixture
def client():
    """Фикстура для тестового клиента FastAPI"""
    return TestClient(app)

@pytest.fixture
def valid_battle_request():
    """Фикстура с валидными данными для создания битвы"""
    return {
        "participant1": {
            "name": "Warrior1",
            "power": 100
        },
        "participant2": {
            "name": "Warrior2",
            "power": 80
        }
    }

@pytest.fixture
def invalid_battle_request_missing_power():
    """Фикстура с невалидными данными (отсутствует power)"""
    return {
        "participant1": {
            "name": "Warrior1"
        },
        "participant2": {
            "name": "Warrior2",
            "power": 80
        }
    }

@pytest.fixture
def invalid_battle_request_negative_power():
    """Фикстура с невалидными данными (отрицательный power)"""
    return {
        "participant1": {
            "name": "Warrior1",
            "power": -100
        },
        "participant2": {
            "name": "Warrior2",
            "power": 80
        }
    }

@pytest.fixture
def battle_id(client, valid_battle_request):
    """Фикстура, создающая битву и возвращающая её ID"""
    response = client.post("/battle/start", json=valid_battle_request)
    return response.json()["battle_id"] 