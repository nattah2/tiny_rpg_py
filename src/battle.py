#!/usr/bin/env python3

# # Usage
# game_events = EventEmitter()
# game_events.on("enemy_death", on_enemy_death)
# game_events.emit("enemy_death", "Goblin")  # Output: "Goblin has been defeated!"

# TODO Please Read This

import event

from abc import ABC, abstractmethod
from typing import Any
from event import *
from character import *
import util

class Battle(EventEmitter):
    def __init__(self, character_list: List[Character], enemy_list: List[Character]):
        super().__init__()
        self.turn_counter: int = 0
        self.is_battle_over: bool = False
        self.character_list = character_list
        self.enemy_list = enemy_list
        self.pool = self.character_list + self.enemy_list

    def start_battle(self):
        """Begin the battle."""
        print("Begin the game")
        self.emit(onBegin(cycle_counter=self.turn_counter))
        self.setup()
        while not self.is_battle_over:
            self.run_turn()
        self.end_battle()

    def setup(self):
        """Initialize battle state, teams, or entities."""
        pass

    def determine_order(self):
        for n in self.pool:
            print(f"{n.name} => {n.stats.speed.value}")


    def run_turn(self):
        """Run a full battle turn cycle."""
        self.turn_counter += 1
        self.emit(onTurnBegin(cycle_counter=self.turn_counter))
        self.handle_turn()
        self.emit(onTurnEnd(cycle_counter=self.turn_counter))
        self.check_battle_end()

    def handle_turn(self):
        """Implement turn logic (attacks, moves, etc.)."""
        print(f"We're doing a turn. It's turn {self.turn_counter}")
        x = input("> ")
        if x == "0":
            self.is_battle_over = True
        if x == "d_speed":
            self.determine_order()
        pass

    def check_battle_end(self):
        """Set `is_battle_over` to True if the battle should end."""
        pass

    def end_battle(self):
        """Cleanup or final events after battle ends."""
        # self.emit(onCycleEnd(cycle_counter=self.turn_counter))
        print("Bye bye!")

    def sanity_check(self):
        if self.turn_counter > 255:
            self.end_battle()

if __name__ == '__main__':
    protag2 = Character(name="Protagonist", stats=Stats(attack=130.0, defense=69.0, speed=88.0))
    protag1 = Character(name="Protagonist", stats=Stats(attack=130.0, defense=69.0, speed=88.0))
    antago1 = Character(name="Antagonist", stats=Stats(attack=130.0, defense=89.0, speed=65.0))
    antago2 = Character(name="Antagonist", stats=Stats(attack=130.0, defense=89.0, speed=65.0))
    util.pprint(protag.model_dump())
    util.pprint(antago.model_dump())
    b = Battle([protag], [antago])
    b.start_battle()
