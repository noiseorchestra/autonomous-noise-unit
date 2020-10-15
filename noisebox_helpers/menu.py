import noisebox_helpers.config as config

main_menu_items = ['CONNECT TO SERVER',
                   'LEVEL METER',
                   'P2P SESSION',
                   'SETTINGS -->']

settings_items = [{"name": "INPUT", "value": "mono"},
                  "IP ADDRESS",
                  "JACKTRIP",
                  "UPDATE",
                  "<-- BACK"]

advanced_settings_items = [{"name": "buffer", "value": "6"}, {"name": "buffer", "value": "6"}, "<-- BACK"]


def get_main_menu_items():
    return main_menu_items

def get_settings_items():
    settings_items[0]["value"] = config.get_config["jacktrip-default"]["input-channels"]
    return settings_items
