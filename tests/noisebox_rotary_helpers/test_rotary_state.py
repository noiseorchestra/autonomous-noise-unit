from noisebox_rotary_helpers.rotary_state import RotaryState_Menu, RotaryState_SettingsMenu, RotaryState_AdvancedSettingsMenu, RotaryState_IpPicker
from unittest.mock import Mock
import noisebox_helpers as nh

input_values = ["1", "2"]
queue_values = ["2", "4", "6", "8"]

menu_items = ['CONNECT TO SERVER',
              'LEVEL METER',
              'P2P SESSION',
              'SETTINGS -->']

settings_menu_items = [{"name": "INPUT", "value": "1"},
                       "IP ADDRESS",
                       "JACKTRIP",
                       "UPDATE",
                       "<-- BACK"]

advanced_settings_items = [{"name": "CHANNELS", "value": "1"}, {"name": "QUEUE", "value": "6"}, "CHANGE IP","<-- BACK"]

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
    oled_menu.settings_items = settings_menu_items
    rotaryState = RotaryState_Menu(debug=True)

    oled_menu.menuindex = 3
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "RotaryState_SettingsMenu"
    oled_menu.new_menu_items.assert_called_with(settings_menu_items)

def test_rotarty_state_settings_menu_item_mono_input():

    oled = Mock()
    oled_menu = Mock()
    noisebox = Mock()

    oled_menu.menu_items = settings_menu_items
    oled_menu.menuindex = 0

    rotaryState = RotaryState_SettingsMenu(debug=True)
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "2"
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "1"
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "2"

def test_rotarty_state_settings_menu_item_jacktrip():

    oled = Mock()
    oled_menu = Mock()
    noisebox = Mock()

    oled_menu.menu_items = settings_menu_items
    oled_menu.advanced_settings_items = advanced_settings_items
    oled_menu.menuindex = 2

    rotaryState = RotaryState_SettingsMenu(debug=True)

    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "RotaryState_AdvancedSettingsMenu"
    oled_menu.new_menu_items.assert_called_with(advanced_settings_items)

def test_rotarty_state_advanced_settings_menu_item_channels():

    oled = Mock()
    oled_menu = Mock()
    noisebox = Mock()

    oled_menu.menu_items = advanced_settings_items
    oled_menu.menuindex = 0

    rotaryState = RotaryState_AdvancedSettingsMenu(debug=True)
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "2"
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "1"
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "2"

def test_rotarty_state_advanced_settings_menu_item_queue():

    oled = Mock()
    oled_menu = Mock()
    noisebox = Mock()

    oled_menu.menu_items = advanced_settings_items
    oled_menu.menuindex = 1

    rotaryState = RotaryState_AdvancedSettingsMenu(debug=True)
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "8"
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "10"
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "12"

def test_rotarty_state_advanced_settings_menu_change_ip():

    oled = Mock()
    oled_menu = Mock()
    noisebox = Mock()

    oled_menu.menu_items = advanced_settings_items
    oled_menu.menuindex = 2

    rotaryState = RotaryState_AdvancedSettingsMenu(debug=True)
    rotaryState.switchCallback(noisebox, oled_menu, oled)
    oled_menu.draw_ip_menu.assert_called_with("0", "")

def test_rotarty_state_ip_picker():
    oled = Mock()
    oled_menu = Mock()
    noisebox = Mock()

    oled_menu.counter = 0
    oled_menu.ip_values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", " ->"]
    oled_menu.ip_address = ""

    rotaryState = RotaryState_IpPicker(debug=True)
    rotaryState.switchCallback(noisebox, oled_menu, oled)
    oled_menu.draw_ip_menu.assert_called_with("0", "")
