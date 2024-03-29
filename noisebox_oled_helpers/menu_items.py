from noisebox_helpers.config import Config

class MenuItems:
    """Class for drawing OLED menu"""

    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self._main_menu_items = ['CONNECT',
                                 'LEVEL METER',
                                 'SETTINGS']
        self._settings_items = [{"name": "INPUT", "value": ""},
                                "DEVICE INFO",
                                "ADVANCED OPTIONS",
                                "UPDATE",
                                'SWITCH OFF',
                                "<-- BACK"]

        self._advanced_settings_items = [{"name": "CHANNELS", "value": ""},
                                         {"name": "QUEUE", "value": ""},
                                         {"name": "IP", "value": ""},
                                         {"name": "FPP", "value": ""},
                                         {"name": "MODE", "value": ""},
                                         {"name": "PEER", "value": ""}, "<-- BACK"]
        self._active_menu_items = self._main_menu_items
        self._input_values = ["1", "2"]
        self._channels_values = ["1", "2"]
        self._queue_values = ["auto", "2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24"]
        self._fpp_values = ["64", "128", "256", "512"]
        self._mode_values = ["hub-server", "p2p"]

    def get_jacktrip_settings(self):
        config = Config(self.dry_run)
        return config.get_config()["jacktrip-default"]

    @property
    def active_menu_items(self):
        return self._active_menu_items

    @property
    def main_menu(self):
        return self._main_menu_items

    @property
    def settings_items(self):
        items = self._settings_items
        items[0]["value"] = self.get_jacktrip_settings()["input-channels"]
        return self._settings_items

    @property
    def advanced_settings_items(self):
        jacktrip_settings = self.get_jacktrip_settings()
        items = self._advanced_settings_items

        items[0]["value"] = jacktrip_settings["jacktrip-channels"]
        items[1]["value"] = jacktrip_settings["jacktrip-q"]
        items[2]["value"] = jacktrip_settings["ip"]
        items[3]["value"] = jacktrip_settings["jack-fpp"]
        items[4]["value"] = jacktrip_settings["jacktrip-mode"]
        items[5]["value"] = jacktrip_settings["peer-ip"]
        return items

    def next_input_value(self):
        return self.next_value(self._input_values, self.settings_items[0]["value"])

    def next_queue_value(self):
        return self.next_value(self._queue_values, self.advanced_settings_items[1]["value"])

    def next_channels_value(self):
        return self.next_value(self._channels_values, self.advanced_settings_items[0]["value"])

    def next_fpp_value(self):
        return self.next_value(self._fpp_values, self.advanced_settings_items[3]["value"])

    def next_mode_value(self):
        return self.next_value(self._mode_values, self.advanced_settings_items[4]["value"])

    def next_value(self, values, current_value):
        index = values.index(current_value)
        next_index = index + 1
        next_index = 0 if next_index == len(values) else next_index
        return values[next_index]

    def set_main_menu(self):
        self._active_menu_items = self._main_menu_items

    def set_advanced_menu(self):
        self._active_menu_items = self.advanced_settings_items

    def set_settings_menu(self):
        self._active_menu_items = self.settings_items

    def set_new_menu_items(self, new_menu_items):
        self._active_menu_items = new_menu_items
