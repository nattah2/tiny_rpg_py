#!/usr/bin/env python3

import pytest
from tinyrpg.character import Character
from tinyrpg.battle import Battle

@pytest.fixture
def character_data():
    c = Character(name="Stink", stats=Stats(attack=100.0, defense=69.0), elo=Elo(), level=Level())
