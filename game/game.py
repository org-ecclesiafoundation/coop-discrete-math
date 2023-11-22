from dataclasses import dataclass
from enum import Enum
from math import sqrt
from typing import List, TypeVar, Union
from copy import deepcopy

T = TypeVar("T")
U = TypeVar("U")

class Result:
    def __init__(self, data: Union[T, None] = None, msg: Union[str, None] = None):
        self.data = data
        self.msg = msg
    def bind(self, f, **kwargs) -> U:
        return f(self, **kwargs)

class Success(Result):
    pass

class Failure(Result):
    pass

def concat_to_msg(r: Result, stuff_to_concat: str = "") -> Result:
    new_result = deepcopy(r)
    if new_result.msg == None:
        new_result.msg = stuff_to_concat
    else:
        new_result.msg += stuff_to_concat
    
    return new_result 

class EventType(Enum):
    Invalid = 0
    Get_Game_State = 1
    Take_Turn = 2
    Move = 3

class Event:
    def __init__(self, current_input: str = ""):
        self.inputs_to_event_type = { 
            "end": EventType.Take_Turn, 
            "status": EventType.Get_Game_State,
            "move": EventType.Move
        }
        self.current_input = current_input.strip()
        self.type = self.inputs_to_event_type.get(self.current_input, EventType.Invalid)

    def choices(self) -> Result:
        keys = self.inputs_to_event_type.keys()
        msg = "Event Choices:\n"
        for key in keys:
             msg += f"  {key}\n"

        return Success(data = keys, msg = msg) 

class Compass_Direction(Enum):
    North     = 1
    Northeast = 2
    East      = 3
    Southeast = 4
    South     = 5
    Southwest = 6
    West      = 7
    Northwest = 8

class Vertical_Direction(Enum):
    Up   = 1
    Down = 2

class Position:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def move_horiz(self, direction: Compass_Direction, distance: float):
        diag_component_dist = distance / sqrt(2)
        match direction:
            case Compass_Direction.North:
                self.y += distance
                return Success()
            case Compass_Direction.Northeast:
                self.y += diag_component_dist
                self.x += diag_component_dist
                return Success()
            case Compass_Direction.East:
                self.x += distance
                return Success()
            case Compass_Direction.Southeast:
                self.y -= diag_component_dist
                self.x += diag_component_dist
                return Success()
            case Compass_Direction.South:
                self.y -= distance
                return Success()
            case Compass_Direction.Southwest:
                self.y -= diag_component_dist
                self.x -= diag_component_dist
                return Success()
            case Compass_Direction.West:
                self.x -= distance
                return Success()
            case Compass_Direction.Northwest:
                self.y += diag_component_dist
                self.x -= diag_component_dist
                return Success()
            case _ :
                return Failure(msg=f"Invalid direction '{direction}'")

    def move_vert(self, direction: Vertical_Direction, distance: float):
        match direction:
            case Vertical_Direction.Up:
                self.z += distance
                return Success()
            case Vertical_Direction.Down:
                self.z -= distance
                return Success()
            case _ :
                return Failure(msg=f"Invalid direction '{direction}'")

class Player:
    def __init__(self, name: str = "Foo Bar"):
        self.name = name.upper()
        self.position = Position(0,0,0)
    def __str__(self):
        return f'''Name: {self.name}
  Position:
    X-Coordinate: {self.position.x}
    Y-Coordinate: {self.position.y}
    Z-Coordinate: {self.position.z}'''

    def move (self, horiz: Compass_Direction = Compass_Direction.North, horiz_dist: float = 0, vert: Vertical_Direction = Vertical_Direction.Up, vert_dist: float = 0):
        self.position.move_horiz(horiz, horiz_dist)
        self.position.move_vert(vert, vert_dist)

class Players:
    def __init__(self, players: List[Player] = []):
        self.players_list = players

    def __str__(self):
        return "\n".join([str(it) for it in self.players_list]) + "\n"

    def add_player(self, player: Player) -> Result:
        matches = [idx for idx, p in enumerate(self.players_list) if p.name == player.name]
        if len(matches) == 0:
            self.players_list.append(player)
            return Success()
        else:
            return Failure(msg = f"Player {p.name} already exists")

    def how_many(self):
        return len(self.players_list)

    def get_player_by_number(self, player_number: int) -> Result:
        players_count = self.how_many()
        if players_count < player_number or player_number < 1:
            return Failure(msg = f"Index {player_number} out of bounds; There are {players_count} players.")
        else:
            player = self.players_list[player_number - 1]
            return Success(data = player, msg = f"It is now {player.name}'s turn.")

class Game_State:
    def __init__(self, players: Players = Players()):
        self.players = players
        self.player_number = 1

    def __str__(self):
        return str(self.players)

    def add_player(self, player: Player) -> Result:
        return self.players.add_player(player)

    def current_player(self) -> Result:
        return self.players.get_player_by_number(self.player_number)

    def take_turn(self) -> Result:
        self.player_number += 1
        if self.players.how_many() < self.player_number:
            self.player_number = 1
        return Success(data = self).bind(concat_to_msg, stuff_to_concat = self.game_info_string())
    
    def game_info_string(self) -> str:
        return f"{self.current_player().msg}\n{Event().choices().msg}"

    def game_info_result(self) -> Result:
        return Success().bind(concat_to_msg, stuff_to_concat = self.game_info_string())

    def handle(self, event: Event) -> Result:
        match event.type:
            case EventType.Get_Game_State:
                return Success(data = self).bind(concat_to_msg, stuff_to_concat = self.game_info_string())
            case EventType.Take_Turn:
                return self.take_turn()
            case EventType.Move:
                return Failure(msg = "Please implement move.\n").bind(concat_to_msg, stuff_to_concat = self.game_info_string())
            case _ :
                return Failure(msg = f"Invalid Event {event.current_input}\n").bind(concat_to_msg, stuff_to_concat = self.game_info_string())
def main():
    print("Welcome to the game!")
    
    max_players = 8
    player_count = 1
    gs = Game_State()
    while(player_count <= max_players):
        name = input(f"Player {player_count}, Please enter your name, or 'e' for enough: ")
        if name.lower() == 'e':
            break
        else:
            p = Player(name = name)
            result = gs.add_player(p)
            if not isinstance(result, Success):
                print(result.msg)
            else:
                player_count = player_count + 1
                
    print(gs)
    print(gs.game_info_result().msg)

    while True:
        current_input = input("Please take an action (q to quit game): ")
        event = Event(current_input)
        if event.current_input.lower() == "q":
            break
        else:
            result = gs.handle(event)
            print(f"{result.msg}")
    
if __name__ == "__main__":
    main()

