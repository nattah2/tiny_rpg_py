#!/usr/bin/env python3

import util
from pydantic import BaseModel, Field
from typing import Tuple, ClassVar

class Elo(BaseModel):
    rating        :   int = 1000
    rating_dev    : float = 0
    k     : ClassVar[int] = 32 # This is a static variable.

    @staticmethod
    def match_probability_win(Player1_rating: int, Player2_rating: int) -> Tuple[float, float]:
        probability = (1.0 / (1.0 + pow(10, ((Player2_rating - Player1_rating) / 400))))
        return (probability, 1 - probability)

    # @staticmethod
    # def glicko_scaling_func(rating_dev: float):
    #     g = 1 / sqrt(1 + 3 * (rating_dev ** 2) / (3.14 ** 2))
    #     return g

    # @staticmethod
    # TODO I have no idea how GLICKO works, so whoops.
    # def glicko_expected_score(player1: Elo, player2: Elo) -> Tuple[float, float]:
    #     # Expected = 1 / (1 + 10^(-g(RD_i^2 + RD_j^2)(r_i - r_j)/400))
    #     Expected = 1 / (1 + 10^(-glicko_scaling_func(player1.rating_dev**2 + player2.rating_dev**2) * (player1.rating_dev - player2.rating_dev)/400))
    #     return Expected

    @staticmethod
    def update_elo(winner, loser) -> Tuple[int, int]:
        winner_probability, loser_probability = Elo.match_probability_win(winner, loser)
        winner_elo = winner + Elo.k * (1 - winner_probability)
        loser_elo  = loser  + Elo.k * (0 - loser_probability)
        return winner_elo, loser_elo

    def probability_win(self, opponent_rating: int) -> float:
        probability = (1.0 / (1.0 + pow(10, ((self.rating - opponent_rating) / 400))))
        return probability

    def __repr__(self) -> str:
        return f"{self.rating}"

if __name__ == '__main__':
    Bob = Elo(rating=1500, rating_dev=350)
    Joe = Elo(rating=1350, rating_dev=350)
    print(Elo.update_elo(Bob.rating, Joe.rating))
