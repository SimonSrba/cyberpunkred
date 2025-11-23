import character

game = True


# Example Usage: Create 3 dynamically generated weapons
# No base_damage input needed!
w1 = Weapon()
w2 = Weapon()
w3 = Weapon()

o_warrior1 = Warrior("Leonidas", 150, 50, 20, 13)
o_wizard1 = Wizard("Gandalf", 100, 150, 2, 5, w2)
o_enemy1 = Enemy("Hulk", 300, 0, 40, 20, w3)




if __name__ == "__main__":
    print(o_wizard1)