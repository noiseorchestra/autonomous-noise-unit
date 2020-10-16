
main_menu_items = ['CONNECT TO SERVER',
                   'LEVEL METER',
                   'P2P SESSION',
                   'SETTINGS -->']

settings_items = [{"name": "INPUT", "value": "1"},
                  "IP ADDRESS",
                  "JACKTRIP",
                  "UPDATE",
                  "<-- BACK"]

advanced_settings_items = [{"name": "CHANNELS", "value": "1"}, {"name": "QUEUE", "value": "6"}, {"name": "IP", "value": "123.123.123.123"},"<-- BACK"]

input_values = ["1", "2"]
channels_values = ["1", "2"]
queue_values = ["2", "4", "6", "8", "10", "12", "14", "16"]

def get_main_menu_items():
    return main_menu_items

def get_settings_items(config):
    # need to implement loading stored config values
    settings_items[0]["value"] = config.get_config()["jacktrip-default"]["input-channels"]
    return settings_items

def get_advanced_settings_items(config):
    # need to implement loading stored config values
    try:
        config.get_config()["jacktrip-default"]["jacktrip-q"]
        q = config.get_config()["jacktrip-default"]["jacktrip-q"]
    except KeyError:
        print("jacktrip-q key does not exisct, setting default value")
        q = "8"

    advanced_settings_items[0]["value"] = config.get_config()["jacktrip-default"]["jacktrip-channels"]
    advanced_settings_items[1]["value"] = q
    advanced_settings_items[2]["value"] = config.get_config()["jacktrip-default"]["ip"]
    return advanced_settings_items

def next_input_value(current_value):
    return next_value(input_values, current_value)

def next_queue_value(current_value):
    return next_value(queue_values, current_value)

def next_channels_value(current_value):
    return next_value(channels_values, current_value)

def next_value(values, current_value):
    index = values.index(current_value)
    next_index = index + 1
    next_index = 0 if next_index == len(values) else next_index
    return values[next_index]
