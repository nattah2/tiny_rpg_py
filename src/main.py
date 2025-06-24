#!/usr/bin/env python3

from cmd import Cmd
import account
import gacha
import database
import util

act = None

class MyPrompt(Cmd):
    # def do_hello(self, args):
    #     """Says hello. If you provide a name, it will greet you with it."""
    #     if len(args) == 0:
    #         name = 'stranger'
    #     else:
    #         name = args
    #     print("Hello, %s" % name)

    def do_login(self, args):
        if len(args) != 3:
            print("Hey, not right.")
            print(args[1] + " " + args[2])
            return
        username, password = args[1], args[2]
        act = database.authenticate_account(username, password)
    def do_quit(self, args):
        """Quits the program."""
        print("Quitting.")
        raise SystemExit


if __name__ == '__main__':
    prompt = MyPrompt()
    prompt.prompt = '> '
    prompt.cmdloop('Starting prompt...')



# username = "Admin"
# password = "Password"
# act = database.authenticate_account(username, password)
# if act:
#     act.list_characters()
#     act.list_artifact()
# else:
#     util.logger.error("Authentication failed.")
