#!/usr/bin/env python3

from pydantic import BaseModel, field_validator, ValidationError
from typing import Callable, Literal, TypeAlias # Import TypeAlias

CurveType: TypeAlias = Literal["Fast", "Medium"]

CURVE_FUNCTIONS = {
    "Fast": lambda n: int((4 * n ** 3) / 5 + 1),
    "Medium": lambda n: n ** 3 + 1
}

class Level(BaseModel):
    """Defines the attributes for leveling."""

    # The actual curve functions (can be outside the class or staticmethod)

    level: int = 1
    _curve_type_name: CurveType = "Medium"  # Use the TypeAlias directly
    level_cap: int = 80
    _exp_to_nextlevel: int = 0  # Will be calculated in model_post_init
    _exp: int = 0

    def model_post_init(self, __context: any) -> None:
        """
        Called after Pydantic model initialization and validation.
        Use this to perform any additional setup that depends on validated fields.
        """
        # Calculate initial _exp_to_nextlevel based on the chosen curve
        self._exp_to_nextlevel = CURVE_FUNCTIONS[self._curve_type_name](self.level)

    def gain_experience(self, experience: int):
        # Access the actual curve function using the stored name
        current_curve_function = CURVE_FUNCTIONS[self._curve_type_name]

        while self.level_cap >= self.level and experience > 0:
            # Calculate remaining XP needed for the current level
            remaining_xp_forlevel = self._exp_to_nextlevel - self._exp

            if remaining_xp_forlevel <= 0:
                # If already at or past the required XP for the current level
                if self.level < self.level_cap:
                    # Level up if not at cap
                    print(f"Level up! (from {self.level})", repr(self))
                    self.level += 1
                    # Carry over excess XP for the new level
                    self._exp = self._exp - self._exp_to_nextlevel if self._exp >= self._exp_to_nextlevel else 0
                    self._exp_to_nextlevel = current_curve_function(self.level)
                    # Recalculate remaining XP for the new level
                    remaining_xp_forlevel = self._exp_to_nextlevel - self._exp
                    # If after leveling up, there's still more XP than needed for the new level,
                    # this loop iteration will re-evaluate and potentially level up again.
                else:
                    # Already at level cap, no more experience can be gained
                    self._exp = self._exp_to_nextlevel # Cap experience at the maximum for the final level
                    break # Exit the loop

            # Determine how much experience to gain in this step
            gain = min(experience, remaining_xp_forlevel)

            # Handle case where gain would be negative (e.g. if remaining_xp_forlevel was negative)
            if gain < 0:
                gain = 0

            self._exp += gain
            experience -= gain

            # If current experience meets or exceeds the requirement and not at level cap
            if self._exp >= self._exp_to_nextlevel and self.level < self.level_cap:
                # Level up will be handled by the next iteration of the while loop
                # This design means a level up print will occur BEFORE the new level XP is fully assigned.
                # It's typical to print AFTER the new state is set. Let's adjust for that.
                pass # The level up logic is now handled more robustly at the top of the loop
            elif self._exp >= self._exp_to_nextlevel and self.level == self.level_cap:
                 self._exp = self._exp_to_nextlevel # Cap experience at the maximum for the final level
                 break # Exit if at cap and experience requirement met

    def checklevel(self) -> int:
        return self.level

    def __repr__(self) -> str:
        # Get the current curve function by its name
        # We don't necessarily need to call the function here, just display info
        return f"LVL: {self.level} [{self._exp}/{self._exp_to_nextlevel}]"

# Example Usage with Pydantic
if __name__=="__main__":
    try:
        # Valid instantiation
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
