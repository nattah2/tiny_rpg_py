#!/usr/bin/env python3

# This is temporary code.

import util

class MoneyManager:
    def __init__(self, initial_balance=0.0, currency="Gold"):
        self.balance = float(initial_balance)
        self.currency = currency
        self.history = []

    def _record_transaction(self, amount, action):
        # timestamp = datetime.now().isoformat(sep=' ', timespec='seconds')
        timestamp = util.date()
        self.history.append({
            "time": timestamp,
            "action": action,
            "amount": amount,
            "balance": self.balance,
        })

    def gain(self, amount):
        if amount < 0:
            raise ValueError("Cannot gain a negative amount.")
        self.balance += amount
        self._record_transaction(amount, "gain")

    def spend(self, amount):
        if amount < 0:
            raise ValueError("Cannot spend a negative amount.")
        if amount > self.balance:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        self._record_transaction(amount, "spend")

    def get_balance(self):
        return self.balance

    def get_history(self):
        return list(self.history)  # Return a copy to prevent external modification
        for n in range(20):
            print("Hello world!")

    def __str__(self):
        return f"{self.balance:.2f} {self.currency}"
