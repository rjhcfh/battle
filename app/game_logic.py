import random
import uuid
from datetime import datetime
from typing import Dict, Tuple
from schemas import Participant, BattleResult

class BattleService:
    """Сервис для управления битвами"""
    
    def __init__(self):
        self.battles: Dict[str, BattleResult] = {}
    
    def create_battle(self, participant1: Participant, participant2: Participant) -> str:
        """
        Создает новую битву между двумя участниками
        
        Args:
            participant1: Первый участник
            participant2: Второй участник
            
        Returns:
            str: ID созданной битвы
        """
        battle_id = str(uuid.uuid4())
        
        # Определяем победителя
        winner_name, winner_power = self._determine_winner(participant1, participant2)
        
        # Создаем результат битвы
        battle_result = BattleResult(
            id=battle_id,
            participant1=participant1,
            participant2=participant2,
            winner=winner_name,
            winner_power=winner_power,
            created_at=datetime.now(),
            completed=True
        )
        
        # Сохраняем в памяти
        self.battles[battle_id] = battle_result
        
        return battle_id
    
    def get_battle(self, battle_id: str) -> BattleResult:
        """
        Получает результат битвы по ID
        
        Args:
            battle_id: ID битвы
            
        Returns:
            BattleResult: Результат битвы
            
        Raises:
            KeyError: Если битва не найдена
        """
        if battle_id not in self.battles:
            raise KeyError(f"Битва с ID {battle_id} не найдена")
        
        return self.battles[battle_id]
    
    def get_all_battles(self) -> Dict[str, BattleResult]:
        """
        Получает все битвы
        
        Returns:
            Dict[str, BattleResult]: Словарь всех битв
        """
        return self.battles.copy()
    
    def get_battles_count(self) -> int:
        """
        Получает количество битв
        
        Returns:
            int: Количество битв
        """
        return len(self.battles)
    
    def _determine_winner(self, participant1: Participant, participant2: Participant) -> Tuple[str, int]:
        """
        Определяет победителя битвы
        
        Args:
            participant1: Первый участник
            participant2: Второй участник
            
        Returns:
            Tuple[str, int]: (имя победителя, сила победителя)
        """
        total_power = participant1.power + participant2.power
        
        if total_power == 0:
            # Если общая сила равна 0, выбираем случайно
            winner = random.choice([participant1, participant2])
        else:
            # Вероятность победы пропорциональна силе участника
            probability1 = participant1.power / total_power
            if random.random() < probability1:
                winner = participant1
            else:
                winner = participant2
        
        return winner.name, winner.power

# Глобальный экземпляр сервиса
battle_service = BattleService() 