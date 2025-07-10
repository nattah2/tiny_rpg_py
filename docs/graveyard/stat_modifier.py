#!/usr/bin/env python3

from tinyrpg.effect import Effect
from tinyrpg.event import EventEmitter, onApply
from typing import Any

class StatModifier(Effect):
    def __init__(self,
                 emitter: EventEmitter,
                 target: Any,
                 name: str = "unnamed",
                 duration_counter: int = -1,
                 flat_value: float = 0.0,
                 mult_value:float  = 1.0
                 ):
        super().__init__(emitter, target, name, duration_counter)
        self.flat_value = flat_value
        self.mult_value = mult_value

    def onApply(self, event: onApply):
        print(f"\n==={self.name}===")
        print(f"\nWe're targeting: {self.target.name}")
        print(f"It has the value: {self.target.value}")
        print(f"We're on turn cycle: {event.cycle_counter}")
