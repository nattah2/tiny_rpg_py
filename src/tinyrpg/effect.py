#!/usr/bin/env python3

from __future__ import annotations
from typing import Any, List, Optional, TYPE_CHECKING
from tinyrpg import util
from tinyrpg.event import EventEmitter, onTurnBegin, onTurnEnd, onAttackDeclaration, onDamage, onBegin, onCycleEnd, onApply
if TYPE_CHECKING:
    from tinyrpg.stats import Stat

class EffectComponent():
    def __init__(self, target: Any, parent: Optional[Effect]):
        self.target = target
        self.parent = parent

    def onTurnBegin(self, event: onTurnBegin): pass
    def onTurnEnd(self, event: onTurnEnd): pass
    def onAttackDeclaration(self, event: onAttackDeclaration): pass
    def onDamage(self, event: onDamage): pass
    def onBegin(self, event: onBegin): pass
    def onCycleEnd(self, event: onCycleEnd): pass
    def onApply(self, event: onApply): pass


class StatModifierComponent(EffectComponent):
    def __init__(self, target: 'Stat', flat_value:float=0.0, mult_value=1.0):
        self.flat_value = flat_value
        self.mult_value = mult_value
        self.target     = target

    def onApply(self, event: onApply):
        print("We're applying to something ...!")
        if self.parent == None:
            util.logger.error("Effect component has no parent.")
            return
        self.target.hook_attach(self.parent)
        print(self.target.value)
        return super().onApply(event)

class Effect():
    """
    Conceptually, an Effect is an Event Listener that responds to events.
    """
    def __init__(self,
                 emitter: EventEmitter,
                 # target: Any,
                 components: List[EffectComponent],
                 name = "unnamed",
                 duration_counter = -1):
        self.emitter = emitter
        # self.target = target
        self.name = name
        self.components = components
        self.duration_counter = duration_counter
        if self.emitter:
            self._register_events()

    def _register_events(self):
        for component in self.components:
            component.parent = self
            self.emitter.on(onTurnBegin, component.onTurnBegin)
            self.emitter.on(onTurnEnd, component.onTurnEnd)
            self.emitter.on(onAttackDeclaration, component.onAttackDeclaration)
            self.emitter.on(onDamage, component.onDamage)
            self.emitter.on(onCycleEnd, component.onCycleEnd)
            self.emitter.on(onApply, component.onApply)

    def _unregister_events(self):
        for component in self.components:
            self.emitter.off(onTurnBegin, component.onTurnBegin)
            self.emitter.off(onTurnEnd, component.onTurnEnd)
            self.emitter.off(onAttackDeclaration, component.onAttackDeclaration)
            self.emitter.off(onDamage, component.onDamage)
            self.emitter.off(onCycleEnd, component.onCycleEnd)
            self.emitter.off(onApply, component.onApply)

    def hook_to(self, target):
        target.hook_attach(self)

# name             : str   = "unnamed"
# duration_counter : int   = 0
# emitter          : EventEmitter

# def model_post_init(self, __context):
#     self._register_events()
# class StatModifier(Effect):
#     def __init__(self,
#                  emitter: EventEmitter,
#                  target: Any,
#                  name: str = "unnamed",
#                  duration_counter: int = -1,
#                  flat_value: float = 0.0,
#                  mult_value:float  = 1.0
#                  ):
#         super().__init__(emitter, target, name, duration_counter)
#         self.flat_value = flat_value
#         self.mult_value = mult_value

#     def onApply(self, event: onApply):
#         print(f"\n==={self.name}===")
#         print(f"\nWe're targeting: {self.target.name}")
#         print(f"It has the value: {self.target.value}")
#         print(f"We're on turn cycle: {event.cycle_counter}")


        # for event_cls in Effect.EVENTS:
        #     method_name = event_cls.__name__  # e.g., "onTurnBegin"
        #     for component in self.components:
        #         handler = getattr(component, method_name, None)
        #         if callable(handler):
        #             self.emitter.on(event_cls, handler)
        # self.emitter.on(onTurnBegin, )


        # self.emitter.off(onTurnBegin, self.onTurnBegin)
        # self.emitter.off(onTurnEnd, self.onTurnEnd)
        # self.emitter.off(onAttackDeclaration, self.onAttackDeclaration)
        # self.emitter.off(onDamage, self.onDamage)
        # self.emitter.off(onCycleEnd, self.onCycleEnd)
        # self.emitter.off(onApply, self.onApply)

    # EVENTS = [
    #     onTurnBegin,
    #     onTurnEnd,
    #     onAttackDeclaration,
    #     onCycleEnd,
    #     onApply
    # ]
