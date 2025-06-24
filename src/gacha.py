#!/usr/bin/env python3

import random
import numpy as np
import money
import json
import database
import account
import util

# For visual purposes.
mapping = {
    "ONE_STAR"   : util.Fore.YELLOW + "★",
    "TWO_STAR"   : util.Fore.YELLOW + "★★",
    "THREE_STAR" : util.Fore.BLUE   + "★★★",
    "FOUR_STAR"  : util.Fore.GREEN  + "★★★★",
    "FIVE_STAR"  : util.Fore.RED    + "★★★★★",
}

class Gacha:
    # sample

    PULL_COST = 3

    def __init__(self, source="./myfile.json"):
        self.source = source

    def read_json(self, file_path=None):
        if file_path is None:
            file_path = self.source
        try:
            with open(file_path, 'r') as json_file:
                util.logger.info(f"Extracting banner data from {file_path}")
                self.json = json.load(json_file)
                self.name = self.json["name"]
                self.schema_version = self.json["schema_version"]
                self.pool = self.json["banner"]
                self.rarities = self.pool.keys()
            for n in self.pool:
                print(n)
            print(self.rarities)
            return self.pool

        except FileNotFoundError:
            exit(f"File not found at path: {file_path}")

        except json.JSONDecodeError:
            exit("Error decoding file. Ensure it is properly formatted JSON.")

        except Exception as e:
            exit(f"An unexpected error occurred: {e}")

    def pull(self, act: account.Account):
        if (act.wallet.get_balance() < Gacha.PULL_COST):
            return
        # TODO ATOMICITY
        act.wallet.spend(Gacha.PULL_COST)
        rarities = self.rarities
        choices = []
        probabilities = []
        for rarity in rarities:
            for option in self.pool[rarity]:
                choices.append((rarity,option))
                probabilities.append(self.pool[rarity][option]["total_rate"])
        which = random.choices(choices, weights=probabilities, k=1)[0]
        ret = (which[0], which[1], random.choices(self.pool[which[0]][which[1]]["list"]))
        if (ret[0] == "FIVE_STAR" and ret[1] == "character"):
            print("------MAJOR PULL!------")
        print(f"{mapping[ret[0]]:<10} | {ret[1]} {ret[2]}")
        # act.add_inventory(ret)
        # if __debug__==True:
        #     util.logger.info(ret)
        # act.save_json()
        return ret

    def ten_pull(self, act: account.Account):
        for n in range(10):
            roll = self.pull(act)
            # print(mapping[roll[0]], end=" ")
            # print(roll[1])
            # print(roll[2])
        print("Bonus!")
        roll = self.pull(act)
        # print(mapping[roll[0]], end=" ")
        # print(roll[1])
        # print(roll[2])


if __name__=="__main__":
    mytestgacha = Gacha()
    mytestgacha.read_json()
    act = database.authenticate_account("Admin", "Password")
    print(act.username)
    print(act.uid)
    print(act.inventory)
    # mytestgacha.ten_pull(act)

    # t = mytestgacha.ten_pull(wallet)
