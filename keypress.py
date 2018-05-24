import logging

from pyHook import HookManager
from pyHook.HookManager import HookConstants


class Keystroke_Watcher:
    def __init__(self, master, sticky=False):
        self.hm = HookManager()
        self.hm.KeyDown = self.on_key_down
        self.hm.KeyUp = self.on_key_up
        self.hm.HookKeyboard()
        self.logger = logging.getLogger(master.logger.name + '.Keystroke_Watcher')
        self.function_map = {}
        self.sticky = sticky

        self.keys_held = set()

    def register_function(self, key_combo, function):
        self.function_map[key_combo.lower()] = function
        self.logger.info(
            "Registered function <{}> to keycombo <{}>.".format(function.__name__, key_combo.lower()))

    def on_key_down(self, event):
        try:
            self.keys_held.add(event.KeyID)
        finally:
            return True

    def get_key_combo_code(self):
        return '+'.join([HookConstants.IDToName(key) for key in self.keys_held])

    def on_key_up(self, event):
        keycombo = self.get_key_combo_code().lower()
        try:
            if keycombo in self.function_map.keys():
                self.logger.info(
                    "Shortcut <{}> pressed. Calling function <{}>.".format(keycombo,
                                                                           self.function_map[keycombo].__name__))
                self.function_map[keycombo]()
        finally:
            if not self.sticky:
                self.keys_held.remove(event.KeyID)
            return True

    def shutdown(self):
        self.hm.UnhookKeyboard()

    def restart(self):
        self.keys_held = set()
        self.hm.HookKeyboard()
