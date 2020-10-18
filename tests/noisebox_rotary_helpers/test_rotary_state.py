from noisebox_rotary_helpers.rotary_state import RotaryState, RotaryState_Menu, RotaryState_SettingsMenu, RotaryState_AdvancedSettingsMenu, RotaryState_IpPicker, RotaryState_PeersMenu
from unittest.mock import Mock
import noisebox_helpers as nh
from noisebox_oled_helpers.menu_items import MenuItems

peers_menu = ["START SERVER", "pi@raspberry1.myvpn", "pi@raspberry2.myvpn", "<-- BACK"]

def test_rotarty_state_menu_item_connect_server():

    noisebox = Mock()
    noisebox.menu = MenuItems()
    noisebox.menu.menuindex = 0
    noisebox.start_jacktrip_session.side_effect = [nh.NoiseBoxCustomError("Error"), True]
    rotaryState = RotaryState_Menu(debug=True)

    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_Scrolling"
    noisebox.oled.start_scrolling_text.assert_called_with("Error")

    rotaryState = RotaryState_Menu(debug=True)
    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_JacktripRunning"


def test_rotarty_state_menu_item_monitoring():

    noisebox = Mock()
    noisebox.menu = MenuItems()
    noisebox.menu.menuindex = 1
    noisebox.start_local_monitoring.side_effect = [nh.NoiseBoxCustomError("Error"), True]
    rotaryState = RotaryState_Menu(debug=True)

    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_Scrolling"
    noisebox.oled.start_scrolling_text.assert_called_with("Error")

    rotaryState = RotaryState_Menu(debug=True)
    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_Monitoring"


def test_rotarty_state_menu_item_p2p():

    noisebox = Mock()
    noisebox.menu = MenuItems()
    noisebox.menu.new_menu_items = Mock()
    noisebox.menu.draw_menu = Mock()
    noisebox.menu.menuindex = 2
    rotaryState = RotaryState_Menu(debug=True)
    noisebox.check_peers.return_value = ['123.123.123.123']

    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_PeersMenu"
    noisebox.menu.new_menu_items.assert_called_with(['123.123.123.123', 'START SERVER', '<-- BACK'])


def test_rotarty_state_menu_item_settings():

    noisebox = Mock()
    noisebox.menu = MenuItems()
    noisebox.menu.new_menu_items = Mock()
    noisebox.menu.draw_menu = Mock()
    noisebox.config = nh.Config(dry_run=True)
    rotaryState = RotaryState_Menu(debug=True)
    noisebox.menu.menuindex = 3

    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_SettingsMenu"
    noisebox.menu.new_menu_items.assert_called_with(noisebox.menu.settings_items)

def test_rotarty_state_start_server_session():

    noisebox = Mock()
    noisebox.start_jacktrip_peer_session.side_effect = [nh.NoiseBoxCustomError("Error"), True]
    noisebox.menu.menu_items = peers_menu
    rotaryState = RotaryState_PeersMenu(debug=True)
    noisebox.menu.menuindex = 0

    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_Scrolling"
    noisebox.oled.start_scrolling_text.assert_called_with("Error")

    rotaryState = RotaryState_PeersMenu(debug=True)
    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_JacktripRunning"
    noisebox.start_jacktrip_peer_session.assert_called_with(server=True)

def test_rotarty_state_start_peer_session():

    noisebox = Mock()

    noisebox.start_jacktrip_peer_session.side_effect = [nh.NoiseBoxCustomError("Error"), True]
    noisebox.menu.menu_items = peers_menu
    rotaryState = RotaryState_PeersMenu(debug=True)
    noisebox.menu.menuindex = 1

    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_Scrolling"
    noisebox.oled.start_scrolling_text.assert_called_with("Error")

    rotaryState = RotaryState_PeersMenu(debug=True)
    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_JacktripRunning"
    noisebox.start_jacktrip_peer_session.assert_called_with(peer_address='pi@raspberry1.myvpn', server=False)

def test_rotarty_state_settings_menu_item_mono_input():

    noisebox = Mock()
    noisebox.menu = MenuItems()
    noisebox.menu.menu_items = noisebox.menu.settings_items
    noisebox.menu.menuindex = 0
    noisebox.menu.draw_menu = Mock()
    rotaryState = RotaryState_SettingsMenu(debug=True)

    rotaryState.switchCallback(noisebox)
    assert noisebox.menu.menu_items[0]["value"] == "2"
    rotaryState.switchCallback(noisebox)
    assert noisebox.menu.menu_items[0]["value"] == "1"
    rotaryState.switchCallback(noisebox)
    assert noisebox.menu.menu_items[0]["value"] == "2"


def test_rotarty_state_settings_menu_item_jacktrip():

    def side_effect(arg):
        return arg

    noisebox = Mock()
    noisebox.menu = MenuItems()
    noisebox.menu.menu_items = noisebox.menu.settings_items
    noisebox.menu.new_menu_items = Mock()
    noisebox.menu.draw_menu = Mock()
    noisebox.menu.new_menu_items.side_effect = side_effect
    noisebox.config = nh.Config(dry_run=True)
    noisebox.menu.menuindex = 2
    rotaryState = RotaryState_SettingsMenu(debug=True)

    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_AdvancedSettingsMenu"
    noisebox.menu.new_menu_items.assert_called_with(noisebox.menu.advanced_settings_items)


def test_rotarty_state_advanced_settings_menu_item_channels():

    noisebox = Mock()
    noisebox.menu = MenuItems()
    noisebox.menu.draw_menu = Mock()
    noisebox.menu.menu_items = noisebox.menu.advanced_settings_items
    noisebox.menu.menuindex = 0

    rotaryState = RotaryState_AdvancedSettingsMenu(debug=True)
    rotaryState.switchCallback(noisebox)
    assert noisebox.menu.menu_items[0]["value"] == "2"
    rotaryState.switchCallback(noisebox)
    assert noisebox.menu.menu_items[0]["value"] == "1"
    rotaryState.switchCallback(noisebox)
    assert noisebox.menu.menu_items[0]["value"] == "2"

def test_rotarty_state_advanced_settings_menu_item_queue():

    noisebox = Mock()
    noisebox.menu = MenuItems()
    noisebox.menu.draw_menu = Mock()
    noisebox.menu.menu_items = noisebox.menu.advanced_settings_items
    noisebox.menu.menuindex = 1
    noisebox.config = nh.Config(dry_run=True)

    rotaryState = RotaryState_AdvancedSettingsMenu(debug=True)
    rotaryState.switchCallback(noisebox)
    assert noisebox.menu.menu_items[1]["value"] == "8"
    rotaryState.switchCallback(noisebox)
    assert noisebox.menu.menu_items[1]["value"] == "10"
    rotaryState.switchCallback(noisebox)
    assert noisebox.menu.menu_items[1]["value"] == "12"


def test_rotarty_state_advanced_settings_menu_change_ip():

    noisebox = Mock()
    noisebox.menu = MenuItems()
    noisebox.menu.draw_ip_menu = Mock()
    noisebox.config = nh.Config(dry_run=True)
    noisebox.menu.menu_items = noisebox.menu.advanced_settings_items
    noisebox.menu.menuindex = 2

    rotaryState = RotaryState_AdvancedSettingsMenu(debug=True)
    rotaryState.switchCallback(noisebox)
    noisebox.menu.draw_ip_menu.assert_called_with(" ->", "111.111.111.111")
    assert rotaryState.ip_address == "111.111.111.111"


def test_rotarty_state_ip_picker():

    noisebox = Mock()
    noisebox.menu = MenuItems()
    noisebox.menu.draw_ip_menu = Mock()
    noisebox.menu.draw_menu = Mock()
    noisebox.menu.new_menu_items = Mock()
    noisebox.config = nh.Config(dry_run=True)
    noisebox.menu.menu_items = noisebox.menu.advanced_settings_items
    noisebox.menu.menuindex = 0

    clicks = [1, 7, 3, 10, 4, 2, 10, 3, 8, 1, 10, 2, 2, -1]
    maximum_clicks = [1, 7, 3, 10, 4, 2, 1, 10, 3, 8, 1, 10, 2, 2, 2]

    new_state_mock = Mock()

    rotaryState = RotaryState(debug=True)
    rotaryState.new_state(RotaryState_IpPicker)
    rotaryState.init_ip_menu(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_IpPicker"
    assert rotaryState.ip_address == "111.111.111.111"

    rotaryState.ip_address = ""
    rotaryState.counter = 0
    rotaryState.switchCallback(noisebox)
    noisebox.menu.draw_ip_menu.assert_called_with(" ->", "0")
    rotaryState.counter = 3
    rotaryState.switchCallback(noisebox)
    noisebox.menu.draw_ip_menu.assert_called_with(" ->", "03")
    rotaryState.counter = 7
    rotaryState.switchCallback(noisebox)
    noisebox.menu.draw_ip_menu.assert_called_with(" ->", "037")
    rotaryState.counter = -2
    rotaryState.switchCallback(noisebox)
    noisebox.menu.draw_ip_menu.assert_called_with("<-", "03")

    rotaryState.ip_address = ""
    rotaryState.counter = 0
    rotaryState.new_state = new_state_mock

    for click in clicks:
        rotaryState.counter = click
        rotaryState.switchCallback(noisebox)
    assert rotaryState.ip_address == "173.42.381.22"
    rotaryState.new_state.assert_called_with(RotaryState_AdvancedSettingsMenu)

    rotaryState.ip_address = ""
    rotaryState.counter = 0
    rotaryState.new_state = new_state_mock

    for click in maximum_clicks:
        rotaryState.counter = click
        rotaryState.switchCallback(noisebox)
    assert rotaryState.ip_address == "173.421.381.222"
    rotaryState.new_state.assert_called_with(RotaryState_AdvancedSettingsMenu)
