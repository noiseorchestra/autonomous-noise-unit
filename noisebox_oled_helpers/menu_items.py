from noisebox_helpers.config import Config

class MenuItems:
    """Class for drawing OLED menu"""

    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self._main_menu_items = ['CONNECT TO SERVER',
                                 'LEVEL METER',
                                 'P2P SESSION',
                                 'SETTINGS -->']
        self._settings_items = [{"name": "INPUT", "value": "1"},
                                "IP ADDRESS",
                                "JACKTRIP",
                                "UPDATE",
                                "<-- BACK"]

        self._advanced_settings_items = [{"name": "CHANNELS", "value": "1"}, {"name": "QUEUE", "value": "6"}, {"name": "IP", "value": "123.123.123.123"},"<-- BACK"]
        self._active_menu_items = self._main_menu_items
        self._input_values = ["1", "2"]
        self._channels_values = ["1", "2"]
        self._queue_values = ["2", "4", "6", "8", "10", "12", "14", "16"]

    def get_jacktrip_settings(self):
        config = Config(self.dry_run)
        return config.get_config()["jacktrip-default"]

    @property
    def active_menu_items(self):
        return self._active_menu_items

    @property
    def settings_items(self):
        items = self._settings_items
        items[0]["value"] = self.get_jacktrip_settings()["input-channels"]
        return self._settings_items

    @property
    def advanced_settings_items(self):
        jacktrip_settings = self.get_jacktrip_settings()
        items = self._advanced_settings_items

        try:
            jacktrip_settings["jacktrip-q"]
            q = jacktrip_settings["jacktrip-q"]
        except KeyError:
            print("jacktrip-q key does not exisct, setting default value")
            q = "8"

        items[0]["value"] = jacktrip_settings["jacktrip-channels"]
        items[1]["value"] = q
        items[2]["value"] = jacktrip_settings["ip"]
        return items

    def next_input_value(self):
        return self.next_value(self._input_values, self.settings_items[0]["value"])

    def next_queue_value(self):
        return self.next_value(self._queue_values, self.advanced_settings_items[1]["value"])

    def next_channels_value(self):
        return self.next_value(self._channels_values, self.advanced_settings_items[0]["value"])

    def next_value(self, values, current_value):
        index = values.index(current_value)
        next_index = index + 1
        next_index = 0 if next_index == len(values) else next_index
        return values[next_index]

    def new_menu_items(self, new_menu_items):
        self._active_menu_items = new_menu_items
