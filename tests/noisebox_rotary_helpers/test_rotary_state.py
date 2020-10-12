from noisebox_rotary_helpers.rotary_state import RotaryState_Menu
from unittest.mock import Mock
import noisebox_helpers as nh

menu_items = ['CONNECT TO SERVER',
              'LEVEL METER',
              'P2P SESSION',
              'SETTINGS -->']

settings_menu = ["MONO INPUT",
                 "MONO OUTPUT",
                 "SERVER A",
                 "IP ADDRESS",
                 "UPDATE",
                 "<-- BACK"]

selected_menu_items = []


def test_rotarty_state_menu_item_connect_server():

    oled = Mock()
    oled_menu = Mock()
    noisebox = Mock()

    noisebox.start_jacktrip_session.side_effect = [nh.NoiseBoxCustomError("Error"), True]
    oled_menu.menu_items = menu_items
    rotaryState = RotaryState_Menu(debug=True)

    oled_menu.menuindex = 0
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "RotaryState_Scrolling"
    oled.start_scrolling_text.assert_called_with("Error")
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "RotaryState_JacktripRunning"


def test_rotarty_state_menu_item_monitoring():

    oled = Mock()
    oled_menu = Mock()
    noisebox = Mock()

    noisebox.start_local_monitoring.side_effect = [nh.NoiseBoxCustomError("Error"), True]
    oled_menu.menu_items = menu_items
    rotaryState = RotaryState_Menu(debug=True)

    oled_menu.menuindex = 1
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "RotaryState_Scrolling"
    oled.start_scrolling_text.assert_called_with("Error")
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "RotaryState_Monitoring"


def test_rotarty_state_menu_item_p2p():

    oled = Mock()
    oled_menu = Mock()
    noisebox = Mock()

    oled_menu.menu_items = menu_items
    rotaryState = RotaryState_Menu(debug=True)
    noisebox.check_peers.return_value = ['123.123.123.123']

    oled_menu.menuindex = 2
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "SwitchState_PeersMenu"
    oled_menu.new_menu_items.assert_called_with(['123.123.123.123', 'START SERVER', '<-- BACK'])


def test_rotarty_state_menu_item_settings():

    oled = Mock()
    oled_menu = Mock()
    noisebox = Mock()

    oled_menu.menu_items = menu_items
    oled_menu.settings_items = settings_menu
    rotaryState = RotaryState_Menu(debug=True)

    oled_menu.menuindex = 3
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "RotaryState_SettingsMenu"
    oled_menu.new_menu_items.assert_called_with(settings_menu)
