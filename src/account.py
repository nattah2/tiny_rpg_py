#!/usr/bin/env python3

import datetime
import json
import money
import os
import util
import uuid

class Account:
    def __init__(self, username: str, uid: uuid.UUID):
        self.username = username
        if not uid:
            util.logger.error("Trying to create an invalid Account")
        self.uid = uid
        self.first_login = util.date()
        self.last_login = util.date()
        self.account_level = 1
        self.inventory = []
        self.BASE_PATH = os.getenv("USER_PATH")
        self.DIRECTORY = f"{self.BASE_PATH}/{self.uid}"
        self.SAVE_PATH = f"{self.DIRECTORY}/save.json"
        self.wallet = money.MoneyManager(currency="Saint Quartz")

    def load_json(self):
        if not os.path.exists(self.SAVE_PATH):
            util.logger.warning("Save file does not exist.")
            self.save_json()
        try:
            with open(self.SAVE_PATH, "r") as in_file:
                data = json.load(in_file)
                self.username         = data['username']
                self.uid              = data['uid']
                self.first_login      = data['first_login']
                # self.last_login       = util.date()
                self.inventory        = data['inventory']
                self.wallet           = money.MoneyManager(data['wallet'], "Saint Quartz") # TODO FIX WALLET EXPORT
        except (json.JSONDecodeError, FileNotFoundError, KeyError) as e:
            util.logger.fatal(f"Failed to load account data: {e}")

    def save_json(self):
        data = {
            'username': self.username,
            'uid': str(self.uid),
            'first_login': self.first_login,
            'last_login': self.last_login,
            'inventory': self.inventory,
            'wallet': self.wallet.balance
        }
        os.makedirs(self.DIRECTORY, exist_ok=True)  # Do I need this? Ah well.
        with open(self.SAVE_PATH, "w") as out_file:
            json.dump(data, out_file, indent=6)
            util.logger.info(f"Saved account {self.username}")

    # A simple test to ensure that we can manipulate the state of this 'account' and load it.
    def add_inventory(self, item: str):
        self.inventory.append(item)

    def list_characters(self):
        for n in self.inventory:
            if "character" in n:
                print(n)

    def list_artifact(self):
        for n in self.inventory:
            if "artifact" in n:
                print(n)
