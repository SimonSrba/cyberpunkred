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
# 1. Create a Concrete Class so we can instantiate "V" or "Arasaka Soldier"
class Actor(Character):
    def attack(self):
        pass # We will handle attack logic in the BattleSystem or here
    
    def check_range(self):
        pass 
        
    def update_range(self):
        pass
        
    def display_details(self):
        print(self.__str__())

    def hit_to_roll(self, enemy_dv: int, distance: int):
        """Simple hit roll helper used by the battle system.

        Returns a dict containing the total and breakdown so callers
        (e.g. `Battlefield.resolve_attack`) can inspect the roll.
        """
        # Choose stat based on equipped weapon attribute (e.g., 'REF' or 'BODY')
        stat_value = None
        skill_value = 0

        if self.equipped_weapon:
            # Weapon DB uses key 'atribute' (note the spelling)
            attr_name = getattr(self.equipped_weapon, 'atribute', None)
            if attr_name and hasattr(self, attr_name):
                stat_value = getattr(self, attr_name)

            # Pick a reasonable skill for the equipped weapon
            for candidate in ('handgun', 'rifles', 'brawling', 'melee'):
                if candidate in self.skills:
                    skill_value = self.skills.get(candidate, 0)
                    break

        # Fallbacks
        if stat_value is None:
            stat_value = getattr(self, 'REF', 0)

        # d10 roll
        roll = random.randint(1, 10)
        total = stat_value + skill_value + roll

        return {
            'total': total,
            'roll': roll,
            'stat': stat_value,
            'skill': skill_value,
        }

# 2. Factory to load Character
def create_actor_from_db(key: str) -> Actor:
    if key not in character_database:
        return None
    
    data = character_database[key]
    # Create the Actor
    actor = Actor(data["name"], data["core_stats"])
    
    # Load Skills
    actor.skills = data["skills"]
    
    # Simple logic to auto-equip the first valid weapon found in a "default loadout"
    # For now, we leave them unarmed until Setup assigns gear, 
    # OR you can map specific starting gear in the DB.
    return actor