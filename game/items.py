import random
from abc import abstractmethod

class Item:
    def __init__(self, name: str, itemid, category: str, atribute: str, cost: int, equipable, weight: float = 0.0):
        self.name = name
        self.itemid = itemid
        self.category = category    # e.g. 'Pistol', 'Brawling', 'Heavy'
        self.atribute = atribute
        self.cost = cost
        self.equipable = equipable
        self.weight = weight
        self.abilities = []
        

    def display_details(self):
        """Prints out the item's key statistics."""
        pass

class Weapon(Item):
    def __init__(self, name: str, itemid: int,category: str, atribute: str, cost: int, equipable: bool, damage: str, weight: float, is_equipped:bool, sp_ignore):
        super().__init__(name, itemid, category, atribute, cost, equipable, weight)
        self.damage = damage # e.g. "2d6", "5d6"
        self.abilities = []
        self.is_equipped = is_equipped
        self.sp_ignore = sp_ignore


    def display_details(self):
        """Prints out the item's key statistics."""
        pass
    
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


class Cyberware(Item):
    def __init__(self, name: str, itemid, category: str, atribute: str, cost: int, equipable, humanity_loss, slot: str, weight: float = 0.0):
        super().__init__(name, itemid, category, atribute, cost, equipable, weight)
        self.humanity_loss = humanity_loss 
        self.slot = slot # Body location/system (e.g. 'Neuralware', 'Cyberarm', 'Skin')
        self.is_installed = False

cyberware_database = {
    "body": {
        "sandevistan_mk4": {
            # Time Dilation - Slow time perception for enhanced reflexes.
            "name": "Arasaka Sandevistan MK4",
            "itemid": "CYB-B-001",
            "category": "Bodycyberware",
            "equipable": True,
            "humanity_loss": 4,
            "cost": 20000,           # Must be integer
            "weight": 15.0,
            "rarity": "Uncommon",
            "sp_ignore": 0,
            "abilities": []
        }
    }
}
ranged_DV_table = {
    "pistol": [13, 15, 20, 25, 30, 30, 99, 99],
    "smg": [15, 13, 15, 20, 25, 25, 30, 99],
    "shotgun_auto": [20, 15, 20, 25, 30, 99, 99, 99],
    "shotgun_shell": [13, 15, 20, 25, 99, 35, 99, 99],
    "assault_rifle": [13, 99, 15, 15, 15, 20, 25, 30],
    "assault_rifle_auto": [17, 16, 17, 20, 25, 20, 30, 99],
    "sniper_rifle": [22, 20, 17, 15, 15, 16, 17, 20],
    "crossbow_bow": [30, 25, 20, 20, 20, 22, 99, 99],
    "grenade_launcher": [15, 13, 15, 17, 20, 22, 25, 99],
    "rocket_launcher": [16, 15, 15, 99, 20, 22, 25, 99],
    "thrown_by_hand": [16, 15, 15, 99, 99, 99, 99, 99],
}


def create_item_from_db(category_key: str, item_key: str):
    """Factory function to create Item objects from the database."""
    if category_key in weapon_database and item_key in weapon_database[category_key]:
        data = weapon_database[category_key][item_key]
        return Weapon(
            name=data["name"],
            itemid=data["itemid"],
            category=data["category"],
            atribute=data["atribute"],
            cost=data["cost"],
            equipable=data["equipable"],
            damage=data["damage"],
            weight=data["weight"],
            is_equipped=False,
            sp_ignore=data.get("sp_ignore", 0)
        )
    # Expansion for cyberware or other items can go here
    return None