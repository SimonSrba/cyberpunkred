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
        self.injuries: List[str] = [] # Is only used when is program running
        self.is_dying: bool = False #instance related

        # 4. GEAR & SKILLS
        self.skills: Dict[str, int] = {}
        self.equipped_weapon: Any = None
        self.equipped_armor: Dict[str, Any] = {}
    
    @abstractmethod
    def check_range(self):
        ranges_all = [] #Dodělat logiku programu
        return ranges_all 
    
    @abstractmethod
    def update_range(self):
        #updatene range
        newrange = 1 #logika celého programu dodělat --------
        return newrange

    def hit_to_roll(self) -> Dict[str, Any]:
        success = 0 #dodělat logiku programu
        return success
    @abstractmethod    
    def attack(self):
        attack = 20 #logika celého programu dodělat --------
        return attack
    
    #-------------------------------------- Getters a Setters ---------------------------------------

    def get_name(self):
        return self.name
  
    def set_name(self, new_name):
        self.name = new_name

#-------------------------------------- General Information ---------------------------------------
    def __str__ (self):
        weapon_info = str(self.equipped_weapon) if self.equipped_weapon else "None"
        return f"""
        {self.name}
        class: {(type(self).__name__)}
        hp: {self.hp_current}/{self.max_hp}
        weapon: {weapon_info}
        SP: {self.BODY * 2}
        """
character_database = {
    "v": {
        "name": "V",
        "core_stats": {
            "INT": 6,
            "WILL": 5,
            "COOL": 7,
            "EMP": 4,
            "TECH": 6,
            "REF": 8,
            "DEX": 7,
            "BODY": 6,
            "MOVE": 7
        },
        "skills": {
            "handgun": 6,
            "brawling": 4,
            "rifles": 5
        },
        "equipped_weapon": None,
        "equipped_armor": {
            "head": None,
            "torso": None,
            "arms": None,
            "legs": None
        },
        "inventory": []
    },
    "jackie": {
        "name": "Jackie Welles",
        "core_stats": {
            "INT": 5,
            "WILL": 4,
            "COOL": 6,
            "EMP": 5,
            "TECH": 4,
            "REF": 7,
            "DEX": 6,
            "BODY": 7,
            "MOVE": 6
        },
        "skills": {
            "brawling": 7,
            "melee": 5,
            "handgun": 4
        },
        "equipped_weapon": None,
        "equipped_armor": {
            "head": None,
            "torso": None,
            "arms": None,
            "legs": None
        },
    },
    "arasaka_soldier": {
        "name": "Arasaka Soldier",
        "core_stats": {
            "INT": 4,
            "WILL": 5,
            "COOL": 5,
            "EMP": 3,
            "TECH": 4,
            "REF": 6,
            "DEX": 5,
            "BODY": 6,
            "MOVE": 5
        },
        "skills": {
            "rifles": 6,
            "handgun": 5,
            "brawling": 3
        },
        "equipped_weapon": None,
        "equipped_armor": {
            "head": None,
            "torso": None,
            "arms": None,
            "legs": None
        },
    },
    "adam_smasher": {
        "name": "Adam Smasher",
        "core_stats": {
            "INT": 6,
            "WILL": 6,
            "COOL": 7,
            "EMP": 1,
            "TECH": 7,
            "REF": 9,
            "DEX": 8,
            "BODY": 9,
            "MOVE": 7
        },
        "skills": {
            "rifles": 8,
            "handgun": 7,
            "brawling": 6
        },
        "equipped_weapon": None,
        "equipped_armor": {
            "head": None,
            "torso": None,
            "arms": None,
            "legs": None
        },
    },
}