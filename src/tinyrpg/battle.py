#!/usr/bin/env python3

# # Usage
# game_events = EventEmitter()
# game_events.on("enemy_death", on_enemy_death)
# game_events.emit("enemy_death", "Goblin")  # Output: "Goblin has been defeated!"
# import event

from dataclasses import dataclass, astuple
# from abc import ABC, abstractmethod
from typing import List
# from tinyrpg.stat_modifier import StatModifier
from tinyrpg.event import EventEmitter, Event, onApply, onAttackDeclaration, onBegin, onCycleEnd, onDamage, onTurnBegin, onTurnEnd
from tinyrpg.character import Character
from tinyrpg.effect import Effect, StatModifierComponent
from tinyrpg.stats import Stats
# import tinyrpg.util
import heapq

@dataclass(order=True)
class TurnEntry:
    """Entries in the Battle's turn order list."""
    action_value: int
    char:         Character

class Battle():
    def __init__(self, character_list: List[Character], enemy_list: List[Character]):
        super().__init__()
        self.turn_counter: int = 0
        self.is_battle_over: bool = False
        self.character_list = character_list
        self.enemy_list = enemy_list
        self.pool = self.character_list + self.enemy_list
        self.turn_order = []
        self.emitter = EventEmitter()

    def start_battle(self):
        """Begin the battle."""
        print("Begin the game")
        self.emitter.emit(
            onBegin(cycle_counter=self.turn_counter)
        )
        self.setup()
        while not self.is_battle_over:
            self.run_turn()
        self.end_battle()

    def determine_order(self):
        """
        This system should work like HSR's. The closer action value gets to move first.
        """
        for character in self.pool:
            action_value = int(10000 / character.stats.speed.value)
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
        self.emitter.emit(onTurnBegin(cycle_counter=self.turn_counter))
        self.handle_turn(char)
        self.emitter.emit(onTurnEnd(cycle_counter=self.turn_counter))
        self.check_battle_end()

    def handle_turn(self, character: Character):
        """Implement turn logic (attacks, moves, etc.)."""
        print(f"{self.turn_counter}: {character.name}'s turn.")
        x = input("> ")
        if x == "0":
            self.is_battle_over = True
        if x == "Kos":
            character.apply_effect(
                Effect(
                    emitter     = self.emitter,
                    name        = "Dragon Dance",
                    components  = [
                        StatModifierComponent(
                            target      = character.stats.speed,
                            mult_value=2.0,
                        ),
                        StatModifierComponent(
                            target = character.stats.attack,
                            mult_value=2.0
                        )
                    ]
                )
            )
        action_value = int(100000 / character.stats.speed.value)
        heapq.heappush(self.turn_order, TurnEntry(action_value, character))

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


# print(f"{character.name} \n {character.stats.speed.value} ->", end=" ")
# character.stats.speed.mult_mod_hook_attach(2)
