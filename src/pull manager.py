#!/usr/bin/env python3

# Pull Manager

import readline
from gacha import Gacha
from money import MoneyManager

def main():
    gacha       = Gacha(None)
    wallet      = MoneyManager(initial_balance=5000)
    while True:
        try:
            user_input = input(">>> ")
            if (user_input == "pull"):
                print(gacha.pull(wallet))

            if (user_input == "10pull"):
                gacha.ten_pull(wallet)

            # Exit condition
            if user_input.lower() in ('exit', 'quit'):
                break

        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    # Enable command history
    readline.parse_and_bind('tab: complete')
    main()
    test = Gacha()
