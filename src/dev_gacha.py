#!/usr/bin/env python3

import json
from enum import Enum
import util

class Gacha:
    RARITY = Enum('Rarity', [('ONE_STAR', 1), ('TWO_STAR', 2), ('THREE_STAR', 3), ('FOUR_STAR', 4), ('FIVE_STAR', 5)])

    def __init__(self, name: str, version: str):
        self.name = name
        self.generated_at = util.date()
        self.schema_version = version
        self.banner = {
            "FIVE_STAR": {
                "character": {
                    "total_rate": 0.01,
                    "list": ["Enkidu", "Artoria Pendragon", "Dioscuri", "Mordred", "Arjuna", "Napoleon", "Minamoto no Tametomo", "Karna", "Ivan the Terrible"]
                },
                "artifact": {
                    "total_rate": 0.04,
                    "list": ["Kaleidoscope", "Black Grail", "Another Ending", "Fragments of 2030", "Vessel of the holy Saint", "Origin Bullet", "Ideal Holy King", "Witchcraft", "The One Who Desires Salvation", "Rising Mud Rain"]
                }
            },
            "FOUR_STAR": {
                "character": {
                    "total_rate": 0.10,
                    "list": ["Nero", "Suzuka Gozen", "EMIYA", "Lancelot", "Gawain", "Prince of Lan Ling", "Tristan", "Nezha"]
                },
                "artifact": {
                    "total_rate": 0.18,
                    "list": ["Test1", "Test2"]
                }
            },
            "THREE_STAR": {
                "character": {
                    "total_rate": 0.32,
                    "list": ["Robin Hood", "Asclepius", "Ushiwakamaru", "Spanky", "Antionne", "Abdul", "Dick", "Nubby"]
                },
                "artifact": {
                    "total_rate": 0.35,
                    "list": ["Dredge", "Spinning Tops", "Spider's Web", "Plastic"]
                }
            },
        }

    def add_target(self, name, rarity, pool: str):
        if rarity.name not in self.banner:
            raise KeyError(f"Invalid rarity: {rarity}")
        if pool not in self.banner[rarity.name]:
            raise KeyError(f"Invalid pool: {pool}")
        self.banner[rarity.name][pool]["list"].append(name)

    def to_dict(self):
        export = {
            "name": self.name,
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "banner": self.banner,
        }
        return export

    def check_probabilities(self):
        total = 0
        for rarity in self.banner.values():
            for pool in rarity.values():
                total += pool["total_rate"]
        return total

    def save_to_file(self, path="myfile.json"):
        if not abs(self.check_probabilities() - 1.0) < util.EPSILON:
            raise ValueError(f"Total probabilities sum to {self.check_probabilities()}, not 1.0")
        with open(path, 'w', encoding='utf8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=True)

def main():
    g = Gacha("Standard", "0.0.0")
    g.add_target("Alpha", Gacha.RARITY.FOUR_STAR, "character")
    g.save_to_file()

if __name__ == '__main__':
    main()
