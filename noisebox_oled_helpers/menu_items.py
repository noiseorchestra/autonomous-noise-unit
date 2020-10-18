class MenuItems:
    """Class for drawing OLED menu"""

    def __init__(self):
        self.main_menu_items = ['CONNECT TO SERVER',
                                'LEVEL METER',
                                'P2P SESSION',
                                'SETTINGS -->']
        self.settings_items = [{"name": "INPUT", "value": "1"},
                               "IP ADDRESS",
                               "JACKTRIP",
                               "UPDATE",
                               "<-- BACK"]

        self.advanced_settings_items = [{"name": "CHANNELS", "value": "1"}, {"name": "QUEUE", "value": "6"}, {"name": "IP", "value": "123.123.123.123"},"<-- BACK"]
        self.input_values = ["1", "2"]
        self.channels_values = ["1", "2"]
        self.queue_values = ["2", "4", "6", "8", "10", "12", "14", "16"]
        self.active_menu_items = self.main_menu_items

    def get_main_menu_items(self):
        return self.active_menu_items

    def get_settings_items(self, config):
        # need to implement loading stored config values
        self.settings_items[0]["value"] = config.get_config()["jacktrip-default"]["input-channels"]
        return self.settings_items

    def get_advanced_settings_items(self, config):
        # need to implement loading stored config values
        try:
            config.get_config()["jacktrip-default"]["jacktrip-q"]
            q = config.get_config()["jacktrip-default"]["jacktrip-q"]
        except KeyError:
            print("jacktrip-q key does not exisct, setting default value")
            q = "8"

        self.advanced_settings_items[0]["value"] = config.get_config()["jacktrip-default"]["jacktrip-channels"]
        self.advanced_settings_items[1]["value"] = q
        self.advanced_settings_items[2]["value"] = config.get_config()["jacktrip-default"]["ip"]
        return self.advanced_settings_items

    def next_input_value(self, current_value):
        return self.next_value(self.input_values, current_value)

    def next_queue_value(self, current_value):
        return self.next_value(self.queue_values, current_value)

    def next_channels_value(self, current_value):
        return self.next_value(self.channels_values, current_value)

    def next_value(self, values, current_value):
        index = values.index(current_value)
        next_index = index + 1
        next_index = 0 if next_index == len(values) else next_index
        return values[next_index]
