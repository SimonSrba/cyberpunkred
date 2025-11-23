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

    def hit_to_roll(self, enemy_dv: int, distance: int = 0) -> Dict[str, Any]:
        if not self.equipped_weapon:
            # Unarmed default: use BODY and brawling skill
            weapon_category = "unarmed"
            required_attr_name = "BODY"
            range_dv_bonus = 0
        else:
            w = self.equipped_weapon
            # support both dict-style database entries and Weapon objects
            if isinstance(w, dict):
                weapon_category = w.get('category', 'unknown')
                required_attr_name = w.get('atribute', 'DEX')
                # some weapons may define a DV/range penalty as 'dv' or 'dv_bonus'
                range_dv_bonus = w.get('dv', w.get('dv_bonus', 0))
            else:
                weapon_category = getattr(w, 'category', 'unknown')
                required_attr_name = getattr(w, 'atribute', 'DEX')
                range_dv_bonus = getattr(w, 'dv', getattr(w, 'dv_bonus', 0))

        # read attribute value from character (default 0 if missing)
        attribute_value = getattr(self, required_attr_name, 0)

        # determine skill value: try direct category key, then common mappings
        cat_key = weapon_category.lower() if isinstance(weapon_category, str) else str(weapon_category)
        skill_value = 0
        # direct lookup
        skill_value = self.skills.get(cat_key, 0)
        if not skill_value:
            # some simple mappings for common weapon categories
            if 'pistol' in cat_key or 'ranged' in cat_key:
                skill_value = self.skills.get('handgun', 0)
            elif 'brawl' in cat_key or 'melee' in cat_key:
                skill_value = self.skills.get('brawling', 0)

        # For ranged weapons, optionally adjust target DV by range-based bonus
        total_target_dv = enemy_dv + (range_dv_bonus if distance > 0 else 0)

        die = random.randint(1, 10)
        total = die + attribute_value + skill_value

        result = {
            'die': die,
            'attribute': required_attr_name,
            'attribute_value': attribute_value,
            'skill_key': cat_key,
            'skill_value': skill_value,
            'total': total,
            'target_dv': total_target_dv,
            'success': total >= total_target_dv,
        }

        return result
 
    @abstractmethod    
    def attack(self):
        #zkontroluje range od nepřítele
        total_attack = 20 #logika celého programu dodělat --------
        return total_attack
    
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
        weapon_info = str(self.equipped_weapon) if self.equipped_weapon else "None"
        return f"""
        {self.name}
        class: {(type(self).__name__)}
        hp: {self.hp_current}/{self.max_hp}
        weapon: {weapon_info}
        SP: {self.BODY * 2}
        """