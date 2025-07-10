#!/usr/bin/env python3

from __future__ import annotations
from pydantic import BaseModel, PrivateAttr, Field
from typing import Optional, List
from tinyrpg.effect import Effect, StatModifierComponent
# from tinyrpg.stat_modifier import StatModifier

class Stat(BaseModel):
    name: str
    base_stat: float = 1.0
    _hook_list: List['Effect'] = PrivateAttr(default_factory=list)
    value: float = 0.0

    def calc_stat(self):
        # TODO We go traverse the list twice.
        # The reason for this is because we need all the
        # multiplicative mods to apply /before/ the flat mods.
        # But, can we change it so that we traverse the list once?
        final_stat = self.base_stat
        for effect in self._hook_list:
            for component in effect.components:
                if isinstance(component, StatModifierComponent) and component.target == self:
                    final_stat *= component.mult_value
        for effect in self._hook_list:
            for component in effect.components:
                if isinstance(component, StatModifierComponent) and component.target == self:
                    final_stat += component.flat_value
        self.value = final_stat



    def hook_attach(self, hook: Effect):
        self._hook_list.append(hook)
        self.calc_stat()

class Stats(BaseModel):
    attack: Stat = Field(default_factory=lambda: Stat(name="ATK"))
    defense: Stat = Field(default_factory=lambda: Stat(name="DEF"))
    speed: Stat = Field(default_factory=lambda: Stat(name="SPE"))
    crit_rate: Stat = Field(default_factory=lambda: Stat(name="CRR"))
    crit_dmg: Stat = Field(default_factory=lambda: Stat(name="CRD"))
    mana_gain: Stat = Field(default_factory=lambda: Stat(name="MNG", base_stat=100.0))

    def __init__(self,
                 attack: Optional[float] = None,
                 defense: Optional[float] = None,
                 speed: Optional[float] = None,
                 crit_rate: Optional[float] = None,
                 crit_dmg: Optional[float] = None,
                 mana_gain: Optional[float] = None,
                 **data):
        """
        Custom constructor for Stats. The default is 1.0 unless otherwise specified.

        Args:
            attack: Base ATK stat.
            defense: Base DEF stat.
            speed: Base SPE stat.
            crit_rate: Base CRR stat.
            crit_dmg: Base CRD stat.
            mana_gain: Base MNG stat. Default: 100.0
        """
        if attack is not None:
            data['attack'] = Stat(name="ATK", base_stat=attack)
        if defense is not None:
            data['defense'] = Stat(name="DEF", base_stat=defense)
        if speed is not None:
            data['speed'] = Stat(name="SPE", base_stat=speed)
        if crit_rate is not None:
            data['crit_rate'] = Stat(name="CRR", base_stat=crit_rate)
        if crit_dmg is not None:
            data['crit_dmg'] = Stat(name="CRD", base_stat=crit_dmg)
        if mana_gain is not None:
            data['mana_gain'] = Stat(name="MNG", base_stat=mana_gain)
        super().__init__(**data)
        for stat in [self.attack, self.defense, self.speed, self.crit_rate, self.crit_dmg, self.mana_gain]:
            stat.calc_stat()

    def show(self):
        print("\n".join([
            f"{'Attack:':<15}{self.attack.value}",
            f"{'Defense:':<15}{self.defense.value}",
            f"{'Speed:':<15}{self.speed.value}",
            f"{'Crit Rate:':<15}{self.crit_rate.value}",
            f"{'Crit Damage:':<15}{self.crit_dmg.value}",
            f"{'Mana Gain:':<15}{self.mana_gain.value}",
            f"{'Resist A':<15}{0}",
            f"{'Resist B':<15}{0}",
            f"{'Resist C':<15}{0}"
        ]))

    def mod_hook_attach(self, hook):
        """You need to change this to be a part of the character."""
        for stat in vars(self).keys():
            if stat in hook.flags:
                if hook.flags[stat][0] == "flat":
                    self.__dict__[stat].flat_mod_hook_attach(hook)
                elif hook.flags[stat][0] == "mult":
                    self.__dict__[stat].mult_mod_hook_attach(hook)
                else:
                    print(f"Unclarified stat change from {hook.name}. Ignoring.")
                print(f"Attached {hook.name} to {stat}.")

class Health(Stat):
    current_value: float



# _flat_mod_hook: List['Effect'] = PrivateAttr(default_factory=list)
# _mult_mod_hook: List['Effect'] = PrivateAttr(default_factory=list)
# def flat_mod_hook_attach(self, hook: Effect):
#     self._flat_mod_hook.append(hook)
#     # hook.attach(hook)
#     self.calc_stat()

# def mult_mod_hook_attach(self, hook: Effect):
#     """
#     Append a multiplicative stat change to the stat.
#     It takes an Effect hook.
#     """
#     self._mult_mod_hook.append(hook)
#     # hook.attach(hook)
#     self.calc_stat()
