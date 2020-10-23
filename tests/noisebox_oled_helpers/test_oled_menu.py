from noisebox_oled_helpers.menu import Menu
from unittest.mock import Mock

menu_items = ['CONNECT',
              'LEVEL METER',
              'SETTINGS']


def test_get_menu_item_string():

    advanced_menu = [
        "CHANNELS: 2",
        "QUEUE: 6",
        "IP: 111.111.111.111",
        "PPS: 256",
        "MODE: hub-server",
        "PEER: 111.111.111.111",
        "<-- BACK"
    ]

    settings_menu = ["INPUT: stereo",
                     "DEVICE INFO",
                     "ADVANCED OPTIONS",
                     "UPDATE",
                     "<-- BACK"]

    menu = Menu(dry_run=True)
    for i in range(len(menu.active_menu_items)):
        assert menu.get_menu_item_str(i) == menu_items[i]

    menu.set_advanced_menu()
    for i in range(len(menu.advanced_settings_items)):
        assert menu.get_menu_item_str(i) == advanced_menu[i]

    menu.set_settings_menu()
    for i in range(len(menu.settings_items)):
        assert menu.get_menu_item_str(i) == settings_menu[i]

def test_new_menu_items():
    menu = Menu()
    menu.set_new_menu_items(["MENUITEM1"])
    assert menu.active_menu_items == ["MENUITEM1"]
