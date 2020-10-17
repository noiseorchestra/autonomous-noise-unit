from noisebox_helpers import menu, Config

main_menu_items = ['CONNECT TO SERVER',
                   'LEVEL METER',
                   'P2P SESSION',
                   'SETTINGS -->']

settings_items = [{"name": "INPUT", "value": "2"},
                  "IP ADDRESS",
                  "JACKTRIP",
                  "UPDATE",
                  "<-- BACK"]

advanced_settings_items = [{"name": "CHANNELS", "value": "2"}, {"name": "QUEUE", "value": "6"}, {"name": "IP", "value": "111.111.111.111"},"<-- BACK"]

input_values = ["1", "2"]
queue_values = ["2", "4", "6", "8"]

default_path = './tests/test_default_config.ini'
custom_path = './tests/test_custom_config.ini'

config = Config(default_path, custom_path)

def test_get_main_menu_items():
    assert menu.get_main_menu_items() == main_menu_items

def test_get_settings_items():
    assert menu.get_settings_items(config) == settings_items

def test_get_settings_items():
    assert menu.get_advanced_settings_items(config) == advanced_settings_items

def test_next_input_value():
    assert menu.next_value(input_values, "1") == "2"
    assert menu.next_value(input_values, "2") == "1"

def test_next_queue_value():
    assert menu.next_value(queue_values, "2") == "4"
    assert menu.next_value(queue_values, "6") == "8"
    assert menu.next_value(queue_values, "8") == "2"
