#!/usr/bin/env python3

from pydantic import BaseModel, field_validator, ValidationError
from typing import Callable, Literal, TypeAlias

CurveType: TypeAlias = Literal["Fast", "Medium"]

CURVE_FUNCTIONS = {
    "Fast": lambda n: int((4 * n ** 3) / 5 + 1),
    "Medium": lambda n: n ** 3 + 1
}

class Level(BaseModel):
    level: int = 1
    _curve_type_name: CurveType = "Medium"
    level_cap: int = 80
    _exp_to_nextlevel: int = 0
    _exp: int = 0

    def model_post_init(self, __context: any) -> None:
        self._exp_to_nextlevel = CURVE_FUNCTIONS[self._curve_type_name](self.level)

    def gain_experience(self, experience: int):
        current_curve_function = CURVE_FUNCTIONS[self._curve_type_name]

        while self.level_cap >= self.level and experience > 0:
            remaining_xp_forlevel = self._exp_to_nextlevel - self._exp

            if remaining_xp_forlevel <= 0:
                if self.level < self.level_cap:
                    print(f"Level up! (from {self.level})", repr(self))
                    self.level += 1
                    self._exp = self._exp - self._exp_to_nextlevel if self._exp >= self._exp_to_nextlevel else 0
                    self._exp_to_nextlevel = current_curve_function(self.level)
                    remaining_xp_forlevel = self._exp_to_nextlevel - self._exp
                else:
                    self._exp = self._exp_to_nextlevel
                    break

            gain = min(experience, remaining_xp_forlevel)

            if gain < 0:
                gain = 0

            self._exp += gain
            experience -= gain

            if self._exp >= self._exp_to_nextlevel and self.level < self.level_cap:
                pass
            elif self._exp >= self._exp_to_nextlevel and self.level == self.level_cap:
                 self._exp = self._exp_to_nextlevel
                 break

    def checklevel(self) -> int:
        return self.level

    def __repr__(self) -> str:
        return f"LVL: {self.level} [{self._exp}/{self._exp_to_nextlevel}]"

if __name__=="__main__":
    try:
        player_fast = Level(level=1, _curve_type_name="Fast", level_cap=10) # Using field names directly
        print(f"Player Fast Curve (Initial): {player_fast}")
        player_fast.gain_experience(5) # Enough for Level 2
        print(f"Player Fast Curve (After XP): {player_fast}")
        player_fast.gain_experience(10) # Enough for Level 3
        print(f"Player Fast Curve (After more XP): {player_fast}")
        player_fast.gain_experience(100) # Should level up multiple times
        print(f"Player Fast Curve (After much more XP): {player_fast}")


        player_medium = Level(level=1, _curve_type_name="Medium", level_cap=10)
        print(f"\nPlayer Medium Curve (Initial): {player_medium}")
        player_medium.gain_experience(5)
        print(f"Player Medium Curve (After XP): {player_medium}")
        player_medium.gain_experience(100)
        print(f"Player Medium Curve (After more XP): {player_medium}")
        player_medium.gain_experience(1000)
        print(f"Player Medium Curve (After much more XP): {player_medium}")

        # Invalid curve type
        print("\nAttempting invalid curve type:")
        player_invalid = Level(_curve_type_name="InvalidCurve") # This will raise ValidationError

    except ValidationError as e:
        print(f"Validation Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
