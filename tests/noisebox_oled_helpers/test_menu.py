from noisebox_helpers import Config
from noisebox_oled_helpers import MenuItems

main_menu_items = ['CONNECT',
                   'LEVEL METER',
                   'SETTINGS']

settings_items = [{"name": "INPUT", "value": "2"},
                  "DEVICE INFO",
                  "ADVANCED OPTIONS",
                  "UPDATE",
                  "<-- BACK"]

advanced_settings_items = [{"name": "CHANNELS", "value": "2"},
                           {"name": "QUEUE", "value": "6"},
                           {"name": "IP", "value": "111.111.111.111"},
                           {"name": "PPS", "value": "256"},
                           {"name": "MODE", "value": "hub server"},
                           {"name": "PEER", "value": "111.111.111.111"},
                           "<-- BACK"]

input_values = ["1", "2"]
queue_values = ["2", "4", "6", "8"]
pps_values = ["64", "128", "256", "512"]
channels_values = ["1", "2"]
hub_mode_values = [True, False]

menu = MenuItems(dry_run=True)

def test_active_menu_items():
    assert menu.active_menu_items == main_menu_items

def test_get_settings_items():
    assert menu.settings_items == settings_items

def test_get_advanced_settings_items():
    assert menu.advanced_settings_items == advanced_settings_items

def test_next_input_value():
    assert menu.next_value(input_values, "1") == "2"
    assert menu.next_value(input_values, "2") == "1"

def test_next_input_value():
    assert menu.next_input_value() == "1"

def test_next_queue_value():
    assert menu.next_queue_value() == "8"

def test_next_channels_value():
    assert menu.next_channels_value() == "1"

def test_next_pps_value():
    assert menu.next_pps_value() == "512"

def test_next_mode_value():
    assert menu.next_mode_value() == "peer connection"
