import random
from abc import ABC, abstractmethod

class Item(ABC):
    def __init__(self, name: str, itemid, category: str, atribute: str, cost: int, equipable, weight: float = 0.0):
        self.name = name
        self.itemid = itemid
        self.category = category    # e.g. 'Pistol', 'Brawling', 'Heavy'
        self.atribute = atribute
        self.cost = cost
        self.equipable = equipable
        self.weight = weight
        self.abilities = []
        
    @abstractmethod
    def display_details(self):
        """Prints out the item's key statistics."""
        pass

class Weapon(Item):
    def __init__(self, name: str, itemid: int,category: str, atribute: str, cost: str, equipable: bool, damage: str, weight: float, is_equipped:bool, sp_ignore):
        super().__init__(name, itemid, category, atribute, cost, equipable, weight)
        self.damage = damage # e.g. "2d6", "5d6"
        self.abilities = []
        self.is_equipped = is_equipped
        self.sp_ignore = sp_ignore

    @abstractmethod
    def display_details(self):
        """Prints out the item's key statistics."""
        pass
    

class Cyberware(Item):
  def __init__(self, name: str, itemid, category: str, cost: int, equipable, humanity_loss, slot: str, weight: float = 0.0):
        super().__init__(name, itemid, category, cost, equipable, weight)
        self.humanity_loss = humanity_loss 
        self.slot = slot # Body location/system (e.g. 'Neuralware', 'Cyberarm', 'Skin')
        self.is_installed = False
     

weapon_database = { #Having it global is supposedly bad practice
    "ranged": {
        "pistol": {
            "name": "Medium Pistol",
            "itemid": "WPN-R-001",  # Should be string for uniqueness/SKU format
            "category": "Pistol",
            "atribute": "REF",
            "equipable": True,
            "damage": "2d6",
            "cost": 500,           # Must be integer
            "weight": 1.0,
            "rarity": "Common",
            "sp_ignore": 0,
            "abilities": [],
        }
    },
    "melee": {
        "theslammer": {
            "name": "The Slammer",
            "itemid": "WPN-M-001",
            "category": "Brawling",
            "atribute": "BODY",
            "equipable": True,
            "damage": "3d6",
            "cost": 500,
            "weight": 6.5,
            "rarity": "Iconic",
            "sp_ignore": 4,
            "abilities": [
                "Ignores 4 SP due to blunt force." # Store the ability as a string
            ]
        }
    }
}

cyberware_database = {
    "body": {
        "sandevistan_mk4": {
            "name": "Arasaka Sandevistan MK4",
            "itemid": "CYB-B-001",
            "category": "Pistol",
            "equipable": True,
            "damage": "2d6",
            "cost": 20000,           # Must be integer
            "weight": 25.0,
            "rarity": "Common",
            "sp_ignore": 0,
            "abilities": [],
        }
    }
}