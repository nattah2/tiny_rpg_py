#!/usr/bin/env python3

from dataclasses import dataclass

class Stat:
    def __init__(self, name, base_stat=1.0):
        self.name = name
        self.base_stat = base_stat
        self.flat_mod_hook = []
        self.mult_mod_hook = []
        self.calc_stat()

    def calc_stat(self) -> int:
        final_stat = self.base_stat
        for hook in self.mult_mod_hook:
            final_stat *= hook.value
        for hook in self.flat_mod_hook:
            final_stat += hook.value
        self.value = final_stat
        return final_stat

    def flat_mod_hook_attach(self, hook) -> None:
        self.flat_mod_hook.append(hook)
        # hook.attach(hook)
        self.calc_stat()

    def mult_mod_hook_attach(self, hook):
        self.mult_mod_hook.append(hook)
        # hook.attach(hook)
        self.calc_stat()

@dataclass
class attack(Stat):
    def __init__(self, base_value):
        self.base_value = base_value

@dataclass
class speed(Stat):
    pass

class Stats:
    def __init__(self):
        self.attack     = Stat("ATK")
        self.defense    = Stat("DEF")
        self.speed      = Stat("SPE")
        self.crit_rate  = Stat("CRR")
        self.crit_dmg   = Stat("CRD")
        self.mana_gain  = Stat("MNG", base_stat=100.0)

    def show(self):
        print("\n".join([
            f"{'Attack:':<15}{self.attack.value}",
            f"{'Defense:':<15}{self.defense.value}",
            f"{'Speed:':<15}{self.defense.value}",
            f"{'Crit Rate:':<15}{self.crit_rate.value}",
            f"{'Crit Damage:':<15}{self.crit_dmg.value}",
            f"{'Mana Gain:':<15}{self.mana_gain.value}",
            f"{'Resist A':<15}{0}",
            f"{'Resist B':<15}{0}",
            f"{'Resist C':<15}{0}"
        ]))

class Statsv2:
    def __init__(self, atk):
        self.atk = attack(base_value=atk)
        print(self.atk.base_value)

MyStats = Statsv2(6969)
P = Statsv2(380)
