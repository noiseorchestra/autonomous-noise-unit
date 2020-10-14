from noisebox_oled_helpers.menu import Menu
from unittest.mock import Mock
import noisebox_helpers as nh

menu_items = ['CONNECT TO SERVER',
              'LEVEL METER',
              'P2P SESSION',
              'SETTINGS -->']

settings_menu = ["MONO INPUT",
                 "IP ADDRESS",
                 "JACKTRIP",
                 "UPDATE",
                 "<-- BACK"]

advanced_menu_items = [{"name": "buffer", "value": "6"}]

def test_get_menu_item_string():
    oled = Mock()
    noisebox = Mock()
    oled_menu = Menu(menu_items, settings_menu, advanced_menu_items)
    for i in range(len(menu_items)):
        assert oled_menu.get_menu_item_str(menu_items, i) == menu_items[i]

    for i in range(len(advanced_menu_items)):
        menu_str = advanced_menu_items[i]["name"] + ": " + advanced_menu_items[i]["value"]
        assert oled_menu.get_menu_item_str(advanced_menu_items, i) == menu_str
