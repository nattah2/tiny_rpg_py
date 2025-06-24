#!/usr/bin/env python3

from math import ceil, log

class TournamentNode:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):
        pass

    def remove(self):
        pass

    def inorder(self):
        pass

    def inorder(self):
        pass


class Tournament:
    def __init__(self, player_set, number_eliminations=1):
        self.player_set = player_set
        self.remaining_players = player_set
        self.eliminated_players = []
        self.total_brackets = pow(2, ceil(log(len(player_set))/log(2))) / 2;
        self.byes = (self.total_brackets * 2) - len(player_set)
        print(f"With {len(player_set)} players, we'd expect {self.total_brackets} brackets in round one with {self.byes} byes.")

    def create_brackets(self):
        self.player_set.sort(key=lambda a: a.elo.rating, reverse=True)

a = Tournament(["0"] * 32)
