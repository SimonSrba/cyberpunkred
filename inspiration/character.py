import random
from weapon import *
from abc import ABC, abstractmethod

class Character(ABC):
  def __init__(self, name, max_hp, max_mana, attack, defense, weapon = None):
    self.name = name
    self.max_hp = max_hp
    self.hp = max_hp
    self.max_mana = max_mana
    self.mana = max_mana
    self.attack = attack 
    self.defense = defense
    self.weapon = weapon

  @classmethod
  def create_new_char(cls, name, max_hp, max_mana, attack, defense, weapon = None):
    return cls(name, max_hp, max_mana, attack, defense, weapon = None)
  @staticmethod
  def generuj_nahodne(rozsah = 3):
      return random.randint(1, rozsah)
  def vycasti_nahodny_spell(self):
      nahodny_spell = Character.generuj_nahodne()
      print(f"{self.name} vycástí spell číslo {nahodny_spell}")
      if nahodny_spell >= 2:
          print("fireball")
      else:
          print("blizzard")
  @abstractmethod
  def zautoc(self):
    print(f"{self.name} útočí")
  @abstractmethod
  def heal(self):
    print(f"{self.name} se healuje")
  def get_effective_attack(self):
    """Vypočítá celkový atack power (atack + weapon + další upscalery damage)"""
    total_attack = self.attack
    if self.weapon is not None:
        # Prida k atributu utoku damage zbrane
        total_attack += self.weapon.damage    
    return total_attack

  #----------------------------------Getter and setter----------------------------------
    # Name
  def get_name(self):
    return self.name
  
  def set_name(self, new_name):
    self.name = new_name

      # Max HP
  def get_max_hp(self):
      return self.max_hp
  
  def set_max_hp(self, new_max_hp):
      # Optional: Add validation (e.g., must be > 0)
      if new_max_hp > 0:
          self.max_hp = new_max_hp
      else:
          print("Max HP must be greater than 0.")

  # Current HP
  def get_hp(self):
      return self.hp
  
  def set_hp(self, new_hp):
      # Ensure HP doesn't go below 0 or above max_hp
      if new_hp < 0:
          self.hp = 0
      elif new_hp > self.max_hp:
          self.hp = self.max_hp
      else:
          self.hp = new_hp

  # Max Mana
  def get_max_mana(self):
      return self.max_mana
  
  def set_max_mana(self, new_max_mana):
      # Optional: Add validation (e.g., must be >= 0)
      if new_max_mana >= 0:
          self.max_mana = new_max_mana
      else:
          print("Max Mana cannot be negative.")

  # Current Mana
  def get_mana(self):
      return self.mana
  
  def set_mana(self, new_mana):
      # Ensure mana doesn't go below 0 or above max_mana
      if new_mana < 0:
          self.mana = 0
      elif new_mana > self.max_mana:
          self.mana = self.max_mana
      else:
          self.mana = new_mana

  # Attack
  def get_attack(self):
      return self.attack
  
  def set_attack(self, new_attack):
      # Optional: Add validation
      if new_attack >= 0:
          self.attack = new_attack
      else:
          print("Attack value cannot be negative.")

  # Defense
  def get_defense(self):
      return self.defense
  
  def set_defense(self, new_defense):
      # Optional: Add validation
      if new_defense >= 0:
          self.defense = new_defense
      else:
          print("Defense value cannot be negative.")

  # Weapon
  def get_weapon(self):
      return self.weapon
  
  def set_weapon(self, new_weapon):
      self.weapon = new_weapon

  def __str__ (self):
    weapon_info = str(self.weapon) if self.weapon else "None"
    return f"""
    {self.name}
    class: {(type(self).__name__)}
    hp: {self.hp}/{self.max_hp}
    mana: {self.mana}/{self.max_mana}
    weapon: {weapon_info}
    base attack: {self.attack}
    effective attack: {self.get_effective_attack()}
    defense: {self.defense}
    """





class Enemy(Character):
    def get_name(self):
      return self.name
    
    def set_name(self, new_name):
      self.name = new_name

    def zautoc(self, other):
        print(f"{self.name} the {(type(self).__name__)}: UAAAAGGGGHHHH!!")
        if random.randint(0,100) < other.defense:
            print(f"{other.name} vyblokoval útok!" )
            return
        else:
            other.hp = other.hp - (self.attack - (self.attack*(other.defense/100)))

    def heal(self):
        print(f"{self.name} the {(type(self).__name__)}: zdlábnul kosti po poražených nepřátelých")

    o_enemy1 = Enemy("Hulk", 300, 0, 40, 20)
class Warrior(Character):
    def get_name(self):
      return self.name
    
    def set_name(self, new_name):
      self.name = new_name

    def zautoc(self, other):
        print(f"{self.name} the {(type(self).__name__)}: útočí - For Frodo and for the Aliance!")
        if random.randint(0,100) < other.defense:
            print(f"{other.name} vyblokoval útok!" )
            return
        else:
            other.hp = other.hp - (self.attack - (self.attack*(other.defense/100)))

    def heal(self):
        print(f"{self.name} the {(type(self).__name__)}: cháluje kuře aby se healnul")
class Wizard(Character):
  def __init__(self, name, max_hp, max_mana, attack, defense, weapon = None):
    super().__init__(name, max_hp, max_mana, attack, defense, weapon)

  def get_name(self):
      return self.name
    
  def set_name(self, new_name):
      self.name = new_name

  def zautoc(self, other):
    print(f"{self.name} the {(type(self).__name__)}: útočí svým magickým palcem")
    if random.randint(0,100) < other.defense:
      print(f"{other.name} vyblokoval útok!" )
      return
    else:
      other.hp = other.hp - (self.attack - (self.attack*(other.defense/100)))

  def heal(self):
    print(f"{self.name} the {(type(self).__name__)}: casts ULTRA-MEGA-HEAL")
    heal_for = (self.get_hp + random.randint((self.max_hp/6),(self.max_hp/4)))
    print(f"heal za {heal_for}")