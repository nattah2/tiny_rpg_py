#!/usr/bin/env python3

from colorama import init
from tinyrpg.event import onApply
from termcolor import colored
from tinyrpg import util
from pydantic import BaseModel, Field

from tinyrpg.elo import Elo
from tinyrpg.stats import Stats
from tinyrpg.level import Level
from tinyrpg.event import onApply
from tinyrpg.effect import Effect

class Character(BaseModel):
        name: str
        stats: Stats
        elo: Elo = Field(default_factory=Elo)
        level: Level = Field(default_factory=Level)

        # TODO Consider passingn the emitter in as a parameter,
        #      instead of keeping it in the effect.
        def apply_effect(self, effect: Effect):
                print(f"We're applying the effect: {effect.name}")
                for n in effect.components:
                        print(f"- We're applying this effect to: {n.target}")
                effect.emitter.emit(
                        onApply(
                                cycle_counter = 0,
                        )
                )
