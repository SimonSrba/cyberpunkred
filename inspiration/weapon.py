import random

WEAPON_COMPONENTS = {
    "Rarity": [
        "Common", "Uncommon", "Rare", "Epic", "Legendary"
    ],
    "Condition": [
        "Broken", "Worn", "Fair", "Good", "Pristine"
    ],
    "Material": [
        "Wood", "Iron", "Steel", "Mithril", "Adamantine"
    ],
    "Adjective": [
        "Furious", "Blazing", "Shadow", "Holy", "Vicious", "Silent", "Ancestral"
    ],
    "Category": [
        "Axe", "Mace", "Sword", "Spear", "Bow", "Blade", "Knife", "Staff", "Orb"
    ],
    "Type": [
        "Melee", "Ranged"
    ],
    
    "DAMAGE_RANGES": {
        "Axe": (15, 25), 
        "Mace": (14, 24),
        "Sword": (12, 22),
        "Spear": (10, 18),

        "Bow": (8, 14), 

        "Blade": (8, 12),
        "Knife": (4, 8),
        
        "Staff": (7, 13), 
        "Orb": (5, 10)
    },

    "RARITY_MULTIPLIERS": {
        "Common": 1.0,
        "Uncommon": 1.15,
        "Rare": 1.3,
        "Epic": 1.5,
        "Legendary": 2.0
    }
}


class Weapon:
    
    def __init__(self, name=None):
            self.type = random.choice(WEAPON_COMPONENTS["Type"])
            self.rarity = random.choice(WEAPON_COMPONENTS["Rarity"])
            self.condition = random.choice(WEAPON_COMPONENTS["Condition"])
            self.material = random.choice(WEAPON_COMPONENTS["Material"])
            self.category = random.choice(WEAPON_COMPONENTS["Category"])
            self.base_damage = self._generate_base_damage()
            if self.category == "Bow":
              self.type = "Ranged"
            else:
              self.type = "Melee"
            
            # 3. Generate the dynamic name
            if name is None:
                self.name = self._generate_name()
            else:
                self.name = name

            # 4. Calculate Final Damage (Base Damage + Rarity Multiplier)
            self.damage = self._calculate_final_damage()


    def _generate_base_damage(self):
        """Generates a random base damage within the range defined for the weapon category."""
        
        # Get the (low, high) tuple for the current weapon category
        damage_range = WEAPON_COMPONENTS["DAMAGE_RANGES"].get(self.category, (5, 10))
        
        # Generate a random integer between the low and high values
        return random.randint(damage_range[0], damage_range[1])


    def _generate_name(self):
        """Generates the weapon name based on its random attributes."""
        
        adjective = random.choice(WEAPON_COMPONENTS.get("Adjective", []))
        
        name_parts = [
            self.rarity,
            self.condition,
            self.material,
            adjective,
            self.category
        ]
        
        return " ".join(name_parts)


    def _calculate_final_damage(self):
        """Calculates total damage by applying the rarity multiplier to the base damage."""
        
        multiplier = WEAPON_COMPONENTS["RARITY_MULTIPLIERS"].get(self.rarity, 1.0)
        
        # Apply rarity multiplier
        final_damage = self.base_damage * multiplier
        
        # Optional: Add a flat bonus based on condition (e.g., Pristine)
        if self.condition == "Pristine":
            final_damage += 3
        elif self.condition == "Broken":
              final_damage -= 5 # Penalty for broken gear

        return round(final_damage)
        
    def __str__(self):
        return f"""
        --- {self.name} ---
        Damage: {self.damage} (Base: {self.base_damage})
        Type: {self.type} | Category: {self.category}
        Rarity: {self.rarity} | Condition: {self.condition} | Material: {self.material}
        """