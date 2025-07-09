#!/usr/bin/env python3

# # Usage
# game_events = EventEmitter()
# game_events.on("enemy_death", on_enemy_death)
# game_events.emit("enemy_death", "Goblin")  # Output: "Goblin has been defeated!"

import event

from dataclasses import dataclass, astuple
from abc import ABC, abstractmethod
from typing import Any
from event import *
from character import *
from effect import *
import heapq
import util

@dataclass(order=True)
class TurnEntry:
    """Entries in the Battle's turn order list."""
    action_value: int
    char:         Character

class Battle(EventEmitter):
    def __init__(self, character_list: List[Character], enemy_list: List[Character]):
        super().__init__()
        self.turn_counter: int = 0
        self.is_battle_over: bool = False
        self.character_list = character_list
        self.enemy_list = enemy_list
        self.pool = self.character_list + self.enemy_list
        self.turn_order = []

    def start_battle(self):
        """Begin the battle."""
        print("Begin the game")
        self.emit(onBegin(cycle_counter=self.turn_counter))
        self.setup()
        while not self.is_battle_over:
            self.run_turn()
        self.end_battle()

    def determine_order(self):
        """
        This system should work like HSR's. The closer action value gets to move first.
        """
        for character in self.pool:
            action_value = 10000 / character.stats.speed.value
            heapq.heappush(self.turn_order, TurnEntry(action_value, character))
        # self.print_order()

    def setup(self):
        """Initialize battle state, teams, or entities. Not much here RN"""
        self.determine_order()

    def print_order(self):
        for entry in self.turn_order:
           print(f"{entry.char.name} => {entry.action_value}")

    def run_turn(self):
        """Run a full battle turn cycle."""
        self.turn_counter += 1
        # `char` represents the character whose turn it is, i.e.
        # the character with the lowest action value.
        # all other characters should have their action values reduced by the
        # lowest action value.
        min_av, char = astuple(heapq.heappop(self.turn_order))
        # print(min_av)
        for _char in self.turn_order:
            _char.action_value -= min_av
        heapq.heapify(self.turn_order)
        self.emit(onTurnBegin(cycle_counter=self.turn_counter))
        self.handle_turn(char)
        self.emit(onTurnEnd(cycle_counter=self.turn_counter))
        self.check_battle_end()

    def handle_turn(self, character: Character):
        """Implement turn logic (attacks, moves, etc.)."""
        print(f"{self.turn_counter}: {character.name}'s turn.")
        x = input("> ")
        if x == "0":
            self.is_battle_over = True
        if x == "Speed Up":
            print(f"{character.name} \n {character.stats.speed.value} ->", end=" ")
            character.stats.speed.mult_mod_hook_attach(2)
            print(f"{character.stats.speed.value}")
        heapq.heappush(self.turn_order, TurnEntry(10000 / character.stats.speed.value, character))

    def check_battle_end(self):
        return self.is_battle_over

    def end_battle(self):
        """Cleanup or final events after battle ends."""
        # self.emit(onCycleEnd(cycle_counter=self.turn_counter))
        print("Bye bye!")

    def sanity_check(self):
        if self.turn_counter > 255:
            self.end_battle()

if __name__ == '__main__':
    protag2 = Character(name="First", stats=Stats(attack=130.0, defense=69.0, speed=99.0))
    protag1 = Character(name="Second", stats=Stats(attack=130.0, defense=69.0, speed=88.0))
    antago1 = Character(name="Third", stats=Stats(attack=130.0, defense=89.0, speed=65.0))
    antago2 = Character(name="Fourth", stats=Stats(attack=130.0, defense=89.0, speed=63.0))
    # util.pprint(protag1.model_dump())
    # util.pprint(protag2.model_dump())
    # util.pprint(antago1.model_dump())
    # util.pprint(antago2.model_dump())
    b = Battle([protag1, protag2], [antago1, antago2])
    b.start_battle()
