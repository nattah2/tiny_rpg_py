#!/usr/bin/env python3

"""
Generate random stuff.
"""

import random

WEAPON = ["sword", "shield", "staff", "axe", "bow", "dagger", "hammer",
           "spear", "whip", "scythe", "blade", "flail", "crossbow"]
GERUND = ["shining", "slashing", "dying", "burning", "freezing", "howling",
          "whispering", "screaming", "laughing", "crying", "thundering", "weeping", "invoking", "enduring", "shattering", "flaying", "leaping", "leaking"]
ADJECTIVE = ["solemn", "darkness", "light", "forgotten", "eternal", "cursed",
             "blessed", "fallen", "rising", "abyssal", "celestial", "unholy", "demonic", "draconic", "elemental", "eight-pathed", "chaotic", "infected"]
NOUN = ["star", "calamity", "death", "liquid", "ice", "fire", "void",
        "twilight", "dawn", "dusk", "storm", "shadow", "blood", "souls", "spire", "mountain", "lake"]

class Word:
    def __init__(name, pos, flags):
        self.name = name
        self.pos = pos
        self.flags = flags


FORMAT = [
    "The @WEAPON of @NOUN",
    "The @GERUND @WEAPON",
    "The @GERUND @WEAPON of @NOUN",
    "The @ADJECTIVE @WEAPON",
    "@ADJECTIVE @WEAPON of the @NOUN",
    "The @NOUN's @WEAPON",
    "@GERUND @NOUN @WEAPON",
    "The @ADJECTIVE @GERUND @WEAPON"
]

def GenerateWeapon():
    Name = random.choice(FORMAT)
    for word in ["WEAPON", "GERUND", "ADJECTIVE", "NOUN"]:
        Name = Name.replace(f"@{word}", random.choice(globals()[word]))
    return Name

print(GenerateWeapon())
