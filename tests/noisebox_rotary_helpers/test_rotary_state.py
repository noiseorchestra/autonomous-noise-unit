from noisebox_rotary_helpers.rotary_state import RotaryState_Menu, RotaryState_SettingsMenu, RotaryState_AdvancedSettingsMenu, RotaryState_IpPicker
from unittest.mock import Mock
import noisebox_helpers as nh

input_values = ["1", "2"]
queue_values = ["2", "4", "6", "8"]

menu_items = ['CONNECT TO SERVER',
              'LEVEL METER',
              'P2P SESSION',
              'SETTINGS -->']

settings_menu_items = [{"name": "INPUT", "value": "2"},
                       "IP ADDRESS",
                       "JACKTRIP",
                       "UPDATE",
                       "<-- BACK"]

advanced_settings_items = [{"name": "CHANNELS", "value": "2"},
                           {"name": "QUEUE", "value": "6"},
                           {"name": "IP", "value": "111.111.111.111"},
                           "<-- BACK"]

default_path = './tests/test_default_config.ini'
custom_path = './tests/test_custom_config.ini'


def test_rotarty_state_menu_item_connect_server():

    oled_menu = Mock()
    noisebox = Mock()

    noisebox.start_jacktrip_session.side_effect = [nh.NoiseBoxCustomError("Error"), True]
    noisebox.menu.menu_items = menu_items
    rotaryState = RotaryState_Menu(debug=True)

    noisebox.menu.menuindex = 0
    rotaryState.switchCallback(noisebox, None, None)
    assert rotaryState.__class__.__name__ == "RotaryState_Scrolling"
    noisebox.oled.start_scrolling_text.assert_called_with("Error")

    rotaryState = RotaryState_Menu(debug=True)
    rotaryState.switchCallback(noisebox, None, None)
    assert rotaryState.__class__.__name__ == "RotaryState_JacktripRunning"


def test_rotarty_state_menu_item_monitoring():

    noisebox = Mock()

    noisebox.start_local_monitoring.side_effect = [nh.NoiseBoxCustomError("Error"), True]
    noisebox.menu.menu_items = menu_items
    rotaryState = RotaryState_Menu(debug=True)

    noisebox.menu.menuindex = 1
    rotaryState.switchCallback(noisebox, None, None)
    assert rotaryState.__class__.__name__ == "RotaryState_Scrolling"
    noisebox.oled.start_scrolling_text.assert_called_with("Error")

    rotaryState = RotaryState_Menu(debug=True)
    rotaryState.switchCallback(noisebox, None, None)
    assert rotaryState.__class__.__name__ == "RotaryState_Monitoring"


def test_rotarty_state_menu_item_p2p():

    noisebox = Mock()

    noisebox.menu.menu_items = menu_items
    rotaryState = RotaryState_Menu(debug=True)
    noisebox.check_peers.return_value = ['123.123.123.123']
    noisebox.config = nh.Config(dry_run=True)

    noisebox.menu.menuindex = 2
    rotaryState.switchCallback(noisebox, None, None)
    assert rotaryState.__class__.__name__ == "SwitchState_PeersMenu"
    noisebox.menu.new_menu_items.assert_called_with(['123.123.123.123', 'START SERVER', '<-- BACK'])


def test_rotarty_state_menu_item_settings():

    noisebox = Mock()

    noisebox.menu.menu_items = menu_items
    noisebox.menu.settings_items = settings_menu_items
    noisebox.config = nh.Config(dry_run=True)
    rotaryState = RotaryState_Menu(debug=True)

    noisebox.menu.menuindex = 3
    rotaryState.switchCallback(noisebox, None, None)
    assert rotaryState.__class__.__name__ == "RotaryState_SettingsMenu"
    noisebox.menu.new_menu_items.assert_called_with(settings_menu_items)


def test_rotarty_state_settings_menu_item_mono_input():

    oled = Mock()
    oled_menu = Mock()
    noisebox = Mock()

    oled_menu.menu_items = settings_menu_items
    oled_menu.menuindex = 0
    noisebox.config = nh.Config(dry_run=True)

    rotaryState = RotaryState_SettingsMenu(debug=True)
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "1"
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "2"
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "1"


def test_rotarty_state_settings_menu_item_jacktrip():

    oled = Mock()
    oled_menu = Mock()
    noisebox = Mock()

    oled_menu.menu_items = settings_menu_items
    oled_menu.advanced_settings_items = advanced_settings_items
    oled_menu.menuindex = 2
    noisebox.config = nh.Config(dry_run=True)

    rotaryState = RotaryState_SettingsMenu(debug=True)

    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "RotaryState_AdvancedSettingsMenu"
    oled_menu.new_menu_items.assert_called_with(advanced_settings_items)


def test_rotarty_state_advanced_settings_menu_item_channels():

    oled = Mock()
    oled_menu = Mock()
    noisebox = Mock()

    oled_menu.menu_items = advanced_settings_items
    oled_menu.menuindex = 0
    noisebox.config = nh.Config(dry_run=True)

    rotaryState = RotaryState_AdvancedSettingsMenu(debug=True)
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "1"
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "2"
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "1"


def test_rotarty_state_advanced_settings_menu_item_queue():

    oled = Mock()
    oled_menu = Mock()
    noisebox = Mock()

    oled_menu.menu_items = advanced_settings_items
    oled_menu.menuindex = 1
    noisebox.config = nh.Config(dry_run=True)

    rotaryState = RotaryState_AdvancedSettingsMenu(debug=True)
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "8"
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "10"
    assert rotaryState.switchCallback(noisebox, oled_menu, oled) == "12"


def test_rotarty_state_advanced_settings_menu_change_ip():

    oled = Mock()
    oled_menu = Mock()
    noisebox = Mock()
    noisebox.config = nh.Config(dry_run=True)

    oled_menu.menu_items = advanced_settings_items
    oled_menu.menuindex = 2

    rotaryState = RotaryState_AdvancedSettingsMenu(debug=True)
    rotaryState.switchCallback(noisebox, oled_menu, oled)
    oled_menu.draw_ip_menu.assert_called_with(" ->", "111.111.111.111")
    assert rotaryState.ip_address == "111.111.111.111"


def test_rotarty_state_ip_picker():

    oled = Mock()
    oled_menu = Mock()
    noisebox = Mock()
    noisebox.config = nh.Config(dry_run=True)

    oled_menu.advanced_settings_items = advanced_settings_items
    oled_menu.menu_items = advanced_settings_items
    oled_menu.menuindex = 0

    clicks = [1, 7, 3, 10, 4, 2, 10, 3, 8, 1, 10, 2, 2, -1]
    maximum_clicks = [1, 7, 3, 10, 4, 2, 1, 10, 3, 8, 1, 10, 2, 2, 2]

    new_state_mock = Mock()

    rotaryState = RotaryState_IpPicker(debug=True)
    assert rotaryState.ip_address == "111.111.111.111"
    rotaryState.ip_address = ""
    assert rotaryState.ip_address == ""

    rotaryState.counter = 0
    rotaryState.switchCallback(noisebox, oled_menu, oled)
    oled_menu.draw_ip_menu.assert_called_with(" ->", "0")
    rotaryState.counter = 3
    rotaryState.switchCallback(noisebox, oled_menu, oled)
    oled_menu.draw_ip_menu.assert_called_with(" ->", "03")
    rotaryState.counter = 7
    rotaryState.switchCallback(noisebox, oled_menu, oled)
    oled_menu.draw_ip_menu.assert_called_with(" ->", "037")
    rotaryState.counter = -2
    rotaryState.switchCallback(noisebox, oled_menu, oled)
    oled_menu.draw_ip_menu.assert_called_with("<-", "03")

    rotaryState = RotaryState_IpPicker(debug=True)
    rotaryState.ip_address = ""
    rotaryState.counter = 0
    rotaryState.new_state = new_state_mock

    for click in clicks:
        rotaryState.counter = click
        rotaryState.switchCallback(noisebox, oled_menu, oled)
    assert rotaryState.ip_address == "173.42.381.22"
    rotaryState.new_state.assert_called_with(RotaryState_AdvancedSettingsMenu)

    rotaryState = RotaryState_IpPicker(debug=True)
    rotaryState.ip_address = ""
    rotaryState.counter = 0
    rotaryState.new_state = new_state_mock

    for click in maximum_clicks:
        rotaryState.counter = click
        rotaryState.switchCallback(noisebox, oled_menu, oled)
    assert rotaryState.ip_address == "173.421.381.222"
    rotaryState.new_state.assert_called_with(RotaryState_AdvancedSettingsMenu)
