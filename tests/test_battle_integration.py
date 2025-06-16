import pytest
from fastapi import status
from app.game_logic import battle_service

class TestBattleFlow:
    """Интеграционные тесты полного flow битвы"""

    def test_complete_battle_flow(self, client):
        """
        Тест полного flow битвы:
        1. Создание битвы
        2. Проверка что битва создалась в сервисе
        3. Получение результата
        4. Проверка что результат соответствует ожиданиям
        5. Проверка что статистика сервиса обновилась
        """
        # Начальное состояние
        initial_battles_count = battle_service.get_battles_count()
        
        # 1. Создаем битву
        battle_request = {
            "participant1": {"name": "Strong Warrior", "power": 100},
            "participant2": {"name": "Weak Warrior", "power": 50}
        }
        create_response = client.post("/battle/start", json=battle_request)
        assert create_response.status_code == status.HTTP_200_OK
        battle_id = create_response.json()["battle_id"]
        
        # 2. Проверяем что битва создалась в сервисе
        assert battle_id in battle_service.battles  # Проверяем внутреннее состояние сервиса
        
        # 3. Получаем результат
        result_response = client.get(f"/battle/{battle_id}")
        assert result_response.status_code == status.HTTP_200_OK
        battle_result = result_response.json()
        
        # 4. Проверяем результат
        assert battle_result["participant1"]["name"] == "Strong Warrior"
        assert battle_result["participant2"]["name"] == "Weak Warrior"
        assert battle_result["winner"] == "Strong Warrior"  # Должен победить более сильный воин
        
        # 5. Проверяем обновление статистики
        final_battles_count = battle_service.get_battles_count()
        assert final_battles_count == initial_battles_count + 1

    def test_battle_with_equal_power(self, client):
        """
        Тест битвы с равными силами:
        Проверяем что система корректно обрабатывает случай равных сил
        и выбирает победителя согласно логике
        """
        battle_request = {
            "participant1": {"name": "Equal Warrior 1", "power": 100},
            "participant2": {"name": "Equal Warrior 2", "power": 100}
        }
        
        # Создаем битву
        create_response = client.post("/battle/start", json=battle_request)
        battle_id = create_response.json()["battle_id"]
        
        # Получаем результат
        result_response = client.get(f"/battle/{battle_id}")
        battle_result = result_response.json()
        
        # Проверяем что победитель определен (согласно бизнес-логике)
        assert "winner" in battle_result
        assert battle_result["winner"] in ["Equal Warrior 1", "Equal Warrior 2"]
        
        # Проверяем что силы участников равны
        assert battle_result["participant1"]["power"] == battle_result["participant2"]["power"]

    def test_multiple_battles_statistics(self, client):
        """
        Тест статистики множественных битв:
        Проверяем что система корректно ведет статистику
        при проведении нескольких битв
        """
        initial_count = battle_service.get_battles_count()
        
        # Проводим несколько битв
        battles = [
            {"p1": {"name": "Warrior1", "power": 100}, "p2": {"name": "Warrior2", "power": 80}},
            {"p1": {"name": "Warrior3", "power": 90}, "p2": {"name": "Warrior4", "power": 95}},
            {"p1": {"name": "Warrior5", "power": 70}, "p2": {"name": "Warrior6", "power": 75}}
        ]
        
        battle_ids = []
        for battle in battles:
            response = client.post("/battle/start", json={
                "participant1": battle["p1"],
                "participant2": battle["p2"]
            })
            battle_ids.append(response.json()["battle_id"])
        
        # Проверяем что все битвы создались
        assert len(battle_ids) == len(battles)
        
        # Проверяем что все битвы доступны
        for battle_id in battle_ids:
            response = client.get(f"/battle/{battle_id}")
            assert response.status_code == status.HTTP_200_OK
        
        # Проверяем обновление статистики
        final_count = battle_service.get_battles_count()
        assert final_count == initial_count + len(battles)
        
        # Проверяем что все битвы сохранились в сервисе
        for battle_id in battle_ids:
            assert battle_id in battle_service.battles 