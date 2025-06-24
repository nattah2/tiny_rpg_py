#!/usr/bin/env python3

from colorama import init
from termcolor import colored
from pydantic import BaseModel
import util

from elo import *
from stats import *
from level import Level

class Character(BaseModel):
        name: str
        stats: Stats
        elo: Elo = Field(default_factory=Elo)
        level: Level = Field(default_factory=Level)


if __name__=="__main__":
        c = Character(name="Stink", stats=Stats(attack=100.0, defense=69.0), elo=Elo(), level=Level())
        util.pprint(c.model_dump())
