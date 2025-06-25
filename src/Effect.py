#!/usr/bin/env python3

from pydantic import BaseModel
from typing import Optional
from stats import Stat
from event import *

class Effect(BaseModel):
    name             : str   = "unnamed"
    duration_counter : int   = 0
    emitter          : EventEmitter

    def model_post_init(self, __context):
        self._register_events()


    def _register_events(self):
        self.emitter.on(onTurnBegin, self._handle_turn_begin)
        self.emitter.on(onTurnBegin, self.onTurnBegin)
        self.emitter.on(onTurnEnd, self.onTurnEnd)
        self.emitter.on(onAttackDeclaration, self.onAttackDeclaration)
        self.emitter.on(onDamage, self.onDamage)
        self.emitter.on(onBegin, self.onBegin)
        self.emitter.on(onCycleEnd, self.onCycleEnd)
        # self.emitter.on(onApply, self.onApply)

    def _unregister_events(self):
        self.emitter.off(onTurnBegin, self._handle_turn_begin)
        self.emitter.off(onTurnBegin, self.onTurnBegin)
        self.emitter.off(onTurnEnd, self.onTurnEnd)
        self.emitter.off(onAttackDeclaration, self.onAttackDeclaration)
        self.emitter.off(onDamage, self.onDamage)
        self.emitter.off(onBegin, self.onBegin)
        self.emitter.off(onCycleEnd, self.onCycleEnd)
        # self.emitter.off(onApply, self.onApply)

    def _handle_turn_begin(self, event: onTurnBegin): pass
    def onTurnBegin(self, event: onTurnBegin): pass
    def onTurnEnd(self, event: onTurnEnd): pass
    def onAttackDeclaration(self, event: onAttackDeclaration): pass
    def onDamage(self, event: onDamage): pass
    def onBegin(self, event: onBegin): pass
    def onCycleEnd(self, event: onCycleEnd): pass


class StatModifier(Effect):
    flat_value       : float = 0.0
    mult_value       : float = 0.0
    hook_to          : Stat
