#!/usr/bin/env python3

class EffectHook():
    def __init__(self, name, value, flags:dict=None):
        self.name     = name
        self.value    = value
        self.lifetime = -1
        self.attach_callback=None
        self.detach_callback = None
        self.flags = {
            "stackable" : 0,
        }
        if flags:
            self.flags.update(flags)
        for key, value in flags.items():
            if key=="attach":
                self.set_attach(value)
            elif key=="detach":
                self.set_detach(value)
            elif key=="lifetime":
                self.lifetime = value
            else:
                self.flags[key] = value
        self.character = None

    def attach(self, character):
        if (self.flags['stackable'] == 1 and self.character != None):
            pass # TODO Add stacking behavior
        self.character = character
        if hasattr(self, "attach_callback"):
            self.attach_callback()
        self.character.stats.mod_hook_attach(self)

    def detach(self):
        if self.character == None:
            return
        if hasattr(self, "detach_callback"):
            self.detach_callback()
        self.character.stats.mod_hook_detach(self)

    def set_attach(self, callback):
        self.attach_callback = callback

    def set_detach(self, callback):
        self.detach_callback = callback

    def on_turn_begin(self):
        pass

    def on_turn_end(self):
        if self.lifetime > 0:
            self.lifetime -= 1
        if self.lifetime <= 0:
            self.detach()

    def on_battle_start(self):
        pass

    def on_attack(self):
        pass

    def on_damage_step(self):
        pass

    def on_receive_damage(self):
        pass

    def o(self):
        print("Hello!")
        detach
