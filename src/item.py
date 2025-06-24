#!/usr/bin/env python3
#
from pydantic import BaseModel

class Test(BaseModel):
    name: str
    elem: int

class Character(BaseModel):
    name: str = "Unnamed"
    level: int = 1
    stats: list[int] = [0]
    test: Test

# Create and validate automatically
data = {
    "name": "Hero",
    "level": "5",  # String gets converted to int
    "test": {"name": "Love", "elem": 128}
}

character = Character(**data)  # Validates and creates object
print(character.model_dump())  # Converts to dict
print(character.model_dump_json())  # Converts to JSON string
