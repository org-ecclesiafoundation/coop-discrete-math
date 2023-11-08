import copy
import pprint

game_state = {
    'player_position': {'x': 0, 'y': 0},
    'inventory': {'coins': 100, 'keys': 1},
    'level': 1,
    'enemies': [{'type': 'goblin', 'hp': 30}, {'type': 'dragon', 'hp': 300}]
}

def game_loop():
    history_of_states = []
    
    for turn in range(3):
        state_snapshot = copy.deepcopy(game_state)
        history_of_states.append(state_snapshot)
        
        game_state['player_position']['x'] += 1
        game_state['player_position']['y'] += 1
        game_state['inventory']['coins'] += 10
        game_state['level'] += 1
        for enemy in game_state['enemies']:
            enemy['hp'] -= 10  # Each enemy takes some damage

        print(f"Turn {turn + 1} completed.")
    
    return history_of_states

history_of_states = game_loop()

def main():
    pp = pprint.PrettyPrinter(indent=4)
    for i, state in enumerate(history_of_states):
        print(f"Snapshot at turn {i + 1}:")
        pp.pprint(state)

if __name__ == "__main__":
    main()

