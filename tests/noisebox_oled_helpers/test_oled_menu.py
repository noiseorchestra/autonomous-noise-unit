from noisebox_oled_helpers.menu import Menu
from unittest.mock import Mock

menu_items = ['CONNECT TO SERVER',
              'LEVEL METER',
              'P2P SESSION',
              'SETTINGS -->']

def test_get_menu_item_string():

    results = [
        "CHANNELS: 2",
        "QUEUE: 6",
        "IP: 111.111.111.111",
        "<-- BACK"
    ]

    menu = Menu(dry_run=True)
    for i in range(len(menu.active_menu_items)):
        assert menu.get_menu_item_str(i) == menu_items[i]

    menu.set_advanced_menu()
    for i in range(len(menu.advanced_settings_items)):
        assert menu.get_menu_item_str(i) == results[i]

def test_new_menu_items():
    menu = Menu()
    menu.set_new_menu_items(["MENUITEM1"])
    assert menu.active_menu_items == ["MENUITEM1"]
