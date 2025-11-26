import items
import entities
from battle_system import Battlefield

def setup_game():
    """5. Game setup: User chooses numbers and characters."""
    bf = Battlefield()
    
    # 1. Load Data Helpers
    # Display available keys for user friendliness
    print("--- Available Characters ---")
    print(", ".join(entities.character_database.keys()))
    print("--- Available Weapons ---")
    # Flattens the nested dict for display
    avail_weapons = []
    for cat in items.weapon_database:
        for w in items.weapon_database[cat]:
            avail_weapons.append(w)
    print(", ".join(avail_weapons))
    print("----------------------------")

    # 2. Setup Blue Team (Allies)
    try:
        blue_count = int(input("How many players on Blue side? "))
    except: blue_count = 1
    
    for i in range(blue_count):
        choice = input(f"Enter DB key for Blue Player {i+1} (e.g., 'v', 'jackie'): ").strip()
        char = entities.create_actor_from_db(choice)
        if not char: 
            print("Invalid key, defaulting to 'v'")
            char = entities.create_actor_from_db('v')
            
        # Give them a weapon for testing
        w_choice = input(f"Weapon for {char.name}? (e.g., 'pistol', 'theslammer'): ").strip()
        # Search which category it belongs to
        found_weapon = None
        for cat in items.weapon_database:
            if w_choice in items.weapon_database[cat]:
                found_weapon = items.create_item_from_db(cat, w_choice)
                break
        
        if found_weapon:
            char.equipped_weapon = found_weapon
            print(f"Equipped {found_weapon.name}")
        
        # Position: Allies start at 0
        bf.add_actor(char, position=0, is_enemy=False)

    # 3. Setup Red Team (Enemies)
    try:
        red_count = int(input("How many players on Red side? "))
    except: red_count = 1
    
    for i in range(red_count):
        choice = input(f"Enter DB key for Red Player {i+1} (e.g., 'arasaka_soldier'): ").strip()
        char = entities.create_actor_from_db(choice)
        if not char:
            print("Defaulting to 'arasaka_soldier'")
            char = entities.create_actor_from_db('arasaka_soldier')
            
        # Default enemy weapon
        w_p = items.create_item_from_db("ranged", "pistol")
        char.equipped_weapon = w_p
        
        # Position: Enemies start 20m away
        bf.add_actor(char, position=20 + (i*5), is_enemy=True)
        
    return bf

def game_loop(bf: Battlefield):
    """6. Main loop and turn based logic."""
    turn_counter = 1
    game_running = True
    
    while game_running:
        print(f"\n=== TURN {turn_counter} ===")
        
        # Combine all participants
        # In a real game, you would sort by Initiative (REF + d10)
        all_actors = bf.allies + bf.enemies
        
        for actor in all_actors:
            if actor.hp_current <= 0: continue # Skip dead
            
            print(f"\n> {actor.name}'s Turn (Pos: {bf.positions[actor]}m, HP: {actor.hp_current})")
            
            # Simple AI / Player check
            if actor in bf.allies:
                action = input("Action? (m)ove / (a)ttack / (p)ass: ").lower()
            else:
                # Basic AI: Always attacks if possible
                action = 'a'
                print("Enemy is attacking!")

            if action == 'm':
                move = int(input("Move how many meters? (negative to go back): "))
                bf.update_position(actor, move)
                
            elif action == 'a':
                # Find closest enemy
                targets = bf.enemies if actor in bf.allies else bf.allies
                valid_targets = [t for t in targets if t.hp_current > 0]
                
                if not valid_targets:
                    print("No targets left!")
                    game_running = False
                    break
                
                # Auto-target closest (Simplification)
                # Sort targets by distance
                valid_targets.sort(key=lambda t: bf.get_distance(actor, t))
                target = valid_targets[0]
                
                print(f"Attacking {target.name} (Dist: {bf.get_distance(actor, target)}m)")
                bf.resolve_attack(actor, target)
                
            elif action == 'p':
                print(f"{actor.name} waits.")
        
        # Check Win Condition
        if not any(a.hp_current > 0 for a in bf.enemies):
            print("\nBlue Team Wins!")
            game_running = False
        elif not any(a.hp_current > 0 for a in bf.allies):
            print("\nRed Team Wins!")
            game_running = False
            
        turn_counter += 1

if __name__ == "__main__":
    battlefield = setup_game()
    game_loop(battlefield)