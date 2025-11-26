from typing import Dict, List
import random
from entities import Actor

class Battlefield:
    def __init__(self):
        # Maps an Actor instance to a position (integer meters)
        self.positions: Dict[Actor, int] = {}
        self.enemies: List[Actor] = []
        self.allies: List[Actor] = []

    def add_actor(self, actor: Actor, position: int, is_enemy: bool):
        """1. Range System: Holds multiple NPCs and PCs."""
        self.positions[actor] = position
        if is_enemy:
            self.enemies.append(actor)
        else:
            self.allies.append(actor)

    def update_position(self, actor: Actor, move_amount: int):
        """1. Range System: Update ranges."""
        if actor in self.positions:
            self.positions[actor] += move_amount
            print(f"{actor.name} moved to {self.positions[actor]}m.")

    def get_distance(self, actor1: Actor, actor2: Actor) -> int:
        """2. Range System: Check ranges."""
        pos1 = self.positions.get(actor1, 0)
        pos2 = self.positions.get(actor2, 0)
        return abs(pos1 - pos2)

    def get_target_dv(self, distance: int, weapon_category: str) -> int:
        """Helper to get Difficulty Value (DV) based on range."""
        # Simplified Cyberpunk Red DV Table
        if weapon_category == "melee" or weapon_category == "brawling":
            return -1 # Special case for contested roll
            
        # Ranged DVs
        if distance <= 6: return 13
        elif distance <= 12: return 15
        elif distance <= 25: return 17
        elif distance <= 50: return 20
        else: return 25

    def resolve_attack(self, attacker: Actor, defender: Actor):
        """3. Check if character is successful to hit."""
        dist = self.get_distance(attacker, defender)
        
        # Determine Weapon Stats
        if not attacker.equipped_weapon:
            print(f"{attacker.name} has no weapon!")
            return

        weapon = attacker.equipped_weapon
        w_cat = weapon.category.lower()
        
        # A. Calculate Attacker Total
        # Uses your existing logic: Stat + Skill + d10
        attack_roll = attacker.hit_to_roll(0, dist) # enemy_dv is calculated below
        attack_total = attack_roll['total']
        
        # B. Calculate Defender Target (DV)
        target_dv = self.get_target_dv(dist, w_cat)
        
        # Special logic: Melee is contested (Attacker vs Defender Evasion)
        if target_dv == -1: 
            # Defender rolls DEX + Evasion + d10
            # Simplified: Assuming 'evasion' skill or generic DEX roll
            defense_roll = random.randint(1, 10) + defender.DEX + defender.skills.get('evasion', 0)
            target_dv = defense_roll
            print(f"Melee Clash! Attacker: {attack_total} vs Defender: {target_dv}")
        else:
            print(f"Ranged Shot! Range: {dist}m | DV needed: {target_dv} | Rolled: {attack_total}")

        # C. Check Success
        if attack_total >= target_dv:
            print("HIT!")
            self.calculate_final_damage(attacker, defender, weapon)
        else:
            print("MISS!")

    def calculate_final_damage(self, attacker: Actor, defender: Actor, weapon):
        """4. Calculate final damage."""
        # Parse damage string e.g., "2d6"
        try:
            num_dice, die_type = map(int, weapon.damage.lower().split('d'))
        except:
            print("Error parsing damage, using default 1d6")
            num_dice, die_type = 1, 6

        # Roll Damage
        dmg_sum = sum(random.randint(1, die_type) for _ in range(num_dice))
        print(f"Damage Roll ({weapon.damage}): {dmg_sum}")

        # Apply Armor (SP)
        # Simplified: Using Body*2 as SP from your __str__ method, or specific armor if you add it
        target_sp = defender.BODY * 2 
        
        # Weapon Armor Penetration (SP Ignore)
        effective_sp = max(0, target_sp - weapon.sp_ignore)
        
        final_damage = max(0, dmg_sum - effective_sp)
        
        defender.hp_current -= final_damage
        print(f"{defender.name} takes {final_damage} damage (Armor soaked {effective_sp}). HP: {defender.hp_current}/{defender.max_hp}")
        
        if defender.hp_current <= 0:
            print(f"{defender.name} has been defeated!")