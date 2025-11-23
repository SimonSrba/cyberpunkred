import random
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class Character(ABC):
    def __init__(self, name: str, core_stats: Dict[str, int]):
        self.name: str = name
        self.role: str = "" # Set in subclasses or later
        # Using .get() for safety, though all 10 are required for character creation
        self.INT: int = core_stats.get('INT', 1)
        self.WILL: int = core_stats.get('WILL', 1)
        self.COOL: int = core_stats.get('COOL', 1)
        self.EMP: int = core_stats.get('EMP', 1)
        self.TECH: int = core_stats.get('TECH', 1)
        self.REF: int = core_stats.get('REF', 1)
        self.DEX: int = core_stats.get('DEX', 1)
        self.BODY: int = core_stats.get('BODY', 1)
        self.LUCK: int = 4 # Starting LUCK is 4-10
        self.MOVE: int = core_stats.get('MOVE', 1)

        #DERIVED
        #these dont have to be in argument because they are calculated either after character creation or they are instance related
        self.max_hp: int = 10 + (5 * self.BODY)
        self.hp_current: int = self.max_hp
        self.max_humanity: int = 10 * self.EMP
        self.humanity_current: int = self.max_humanity 
        self.injuries: List[str] = []
        self.is_dying: bool = False

        # 4. GEAR & SKILLS
        self.skills: Dict[str, int] = {}
        self.equipped_weapon: Any = None
        self.equipped_armor: Dict[str, Any] = {}
    '''
    @abstractmethod    
    def hit_to_roll(self):
        get equiped weapon category
        if equipped weapon == "range"
        - get bonus DV from weapon if it is range (different guns have different DV points)
        - DV = enemy.DV + range_DV_bonus
        
        check = random.randint(1, 10) + required atribute(check from weapons) + Skill(for the type of weapon)

        return 1

    '''
    @abstractmethod    
    def attack(self):
        #zkontroluje range od nepřítele
        total_attack = 1
    
    @abstractmethod
    def check_range(self):
        #checkne range od nepřítele a vrátí jestli je nepřítel v dosahu equipped zbraně
        range = 1
        return range
    
    @abstractmethod
    def update_range(self):
        #updatene range
        newrange = 1 #logika celého programu dodělat --------
        return newrange
    
    #-------------------------------------- Getters a Setters ---------------------------------------

    def get_name(self):
        return self.name
  
    def set_name(self, new_name):
        self.name = new_name

#-------------------------------------- General Information ---------------------------------------
    def __str__ (self):
        weapon_info = str(self.weapon) if self.weapon else "None"
        return f"""
        {self.name}
        class: {(type(self).__name__)}
        hp: {self.hp}/{self.max_hp}
        weapon: {weapon_info}
        SP: {self.defense}
        """

