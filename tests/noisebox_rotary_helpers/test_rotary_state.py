import noisebox_rotary_helpers.rotary_state as rs
from unittest.mock import Mock
import noisebox_helpers as nh
from noisebox_oled_helpers.menu import Menu

peers_menu = ["START SERVER", "pi@raspberry1.myvpn", "pi@raspberry2.myvpn", "<-- BACK"]

def test_rotarty_state_menu_item_connect_server():

    noisebox = Mock()
    noisebox.menu = Menu(dry_run=True)
    noisebox.menu.menuindex = 0
    noisebox.start_jacktrip_session.side_effect = [nh.NoiseBoxCustomError("Error"), True]
    rotaryState = rs.RotaryState_Menu(debug=True)

    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_Scrolling"
    noisebox.oled.start_scrolling_text.assert_called_with("Error")

    rotaryState = rs.RotaryState_Menu(debug=True)
    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_JacktripRunning"


def test_rotarty_state_menu_item_monitoring():

    noisebox = Mock()
    noisebox.menu = Menu(dry_run=True)
    noisebox.menu.menuindex = 1
    noisebox.start_local_monitoring.side_effect = [nh.NoiseBoxCustomError("Error"), True]
    rotaryState = rs.RotaryState_Menu(debug=True)

    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_Scrolling"
    noisebox.oled.start_scrolling_text.assert_called_with("Error")

    rotaryState = rs.RotaryState_Menu(debug=True)
    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_Monitoring"


# def test_rotarty_state_menu_item_p2p():
#
#     noisebox = Mock()
#     noisebox.menu = Menu(dry_run=True)
#     noisebox.menu.set_new_menu_items = Mock()
#     noisebox.menu.draw_menu = Mock()
#     noisebox.menu.menuindex = 2
#     rotaryState = rs.RotaryState_Menu(debug=True)
#     noisebox.check_peers.return_value = ['123.123.123.123']
#
#     rotaryState.switchCallback(noisebox)
#     assert rotaryState.__class__.__name__ == "RotaryState_PeersMenu"
#     noisebox.menu.set_new_menu_items.assert_called_with(['123.123.123.123', 'START SERVER', '<-- BACK'])


def test_rotarty_state_menu_item_settings():

    noisebox = Mock()
    noisebox.menu = Menu(dry_run=True)
    noisebox.menu.set_settings_menu = Mock()
    noisebox.menu.draw_menu = Mock()
    noisebox.config = nh.Config(dry_run=True)
    rotaryState = rs.RotaryState_Menu(debug=True)
    noisebox.menu.menuindex = 2

    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_SettingsMenu"
    noisebox.menu.set_settings_menu.assert_called()

def test_rotarty_state_start_server_session():

    noisebox = Mock()
    noisebox.menu = Menu(dry_run=True)
    noisebox.start_jacktrip_peer_session.side_effect = [nh.NoiseBoxCustomError("Error"), True]
    noisebox.menu.set_new_menu_items(peers_menu)
    rotaryState = rs.RotaryState_PeersMenu(debug=True)
    noisebox.menu.menuindex = 0

    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_Scrolling"
    noisebox.oled.start_scrolling_text.assert_called_with("Error")

    rotaryState = rs.RotaryState_PeersMenu(debug=True)
    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_JacktripRunning"
    noisebox.start_jacktrip_peer_session.assert_called_with(server=True)

def test_rotarty_state_start_peer_session():

    noisebox = Mock()
    noisebox.menu = Menu(dry_run=True)
    noisebox.start_jacktrip_peer_session.side_effect = [nh.NoiseBoxCustomError("Error"), True]
    noisebox.menu.set_new_menu_items(peers_menu)
    rotaryState = rs.RotaryState_PeersMenu(debug=True)
    noisebox.menu.menuindex = 1

    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_Scrolling"
    noisebox.oled.start_scrolling_text.assert_called_with("Error")

    rotaryState = rs.RotaryState_PeersMenu(debug=True)
    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_JacktripRunning"
    noisebox.start_jacktrip_peer_session.assert_called_with(peer_address='pi@raspberry1.myvpn', server=False)

def test_rotarty_state_settings_menu_item_mono_input():

    noisebox = Mock()
    noisebox.menu = Menu(dry_run=True)
    noisebox.menu.set_settings_menu()
    noisebox.menu.draw_menu = Mock()
    noisebox.menu.menuindex = 0
    rotaryState = rs.RotaryState_SettingsMenu(debug=True)
    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_SettingsMenu"
    noisebox.config.change_input_channels.assert_called_with("1")


def test_rotarty_state_settings_menu_item_jacktrip():

    noisebox = Mock()
    noisebox.menu = Menu(dry_run=True)
    noisebox.menu.set_settings_menu()
    noisebox.menu.set_advanced_menu = Mock()
    noisebox.menu.draw_menu = Mock()
    noisebox.config = nh.Config(dry_run=True)
    noisebox.menu.menuindex = 2
    rotaryState = rs.RotaryState_SettingsMenu(debug=True)
    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_AdvancedSettingsMenu"
    noisebox.menu.set_advanced_menu.assert_called()


def test_rotarty_state_advanced_settings_menu_item_channels():

    noisebox = Mock()
    noisebox.menu = Menu(dry_run=True)
    noisebox.menu.draw_menu = Mock()
    noisebox.menu.set_advanced_menu()
    noisebox.menu.menuindex = 0

    rotaryState = rs.RotaryState_AdvancedSettingsMenu(debug=True)
    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_AdvancedSettingsMenu"
    noisebox.config.change_output_channels.assert_called_with("1")

def test_rotarty_state_advanced_settings_menu_item_queue():

    noisebox = Mock()
    noisebox.menu = Menu(dry_run=True)
    noisebox.menu.draw_menu = Mock()
    noisebox.menu.set_advanced_menu()
    noisebox.menu.menuindex = 1

    rotaryState = rs.RotaryState_AdvancedSettingsMenu(debug=True)
    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_AdvancedSettingsMenu"
    noisebox.config.change_queue.assert_called_with("8")

def test_rotarty_state_advanced_settings_menu_item_pps():

    noisebox = Mock()
    noisebox.menu = Menu(dry_run=True)
    noisebox.menu.draw_menu = Mock()
    noisebox.menu.set_advanced_menu()
    noisebox.menu.menuindex = 3

    rotaryState = rs.RotaryState_AdvancedSettingsMenu(debug=True)
    rotaryState.switchCallback(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_AdvancedSettingsMenu"
    noisebox.config.change_jack_pps.assert_called_with("512")

def test_rotarty_state_advanced_settings_menu_change_ip():

    noisebox = Mock()
    noisebox.menu = Menu(dry_run=True)
    noisebox.menu.draw_ip_menu = Mock()
    noisebox.config = nh.Config(dry_run=True)
    noisebox.menu.set_advanced_menu()
    noisebox.menu.menuindex = 2

    rotaryState = rs.RotaryState_AdvancedSettingsMenu(debug=True)
    rotaryState.switchCallback(noisebox)
    noisebox.menu.draw_ip_menu.assert_called_with(" ->", "111.111.111.111")
    assert rotaryState.ip_address == "111.111.111.111"
    assert rotaryState.__class__.__name__ == "RotaryState_IpPicker_Server"


def test_rotarty_state_ip_picker():

    noisebox = Mock()
    noisebox.menu = Menu(dry_run=True)
    noisebox.menu.draw_ip_menu = Mock()
    noisebox.menu.draw_menu = Mock()
    noisebox.menu.reset_menu = Mock()
    noisebox.config = nh.Config(dry_run=True)
    noisebox.menu.set_advanced_menu()
    noisebox.menu.menuindex = 0

    clicks = [1, 7, 3, 10, 4, 2, 10, 3, 8, 1, 10, 2, 2, -1]
    maximum_clicks = [1, 7, 3, 10, 4, 2, 1, 10, 3, 8, 1, 10, 2, 2, 2]

    new_state_mock = Mock()

    rotaryState = rs.RotaryState(debug=True)
    rotaryState.new_state(rs.RotaryState_IpPicker_Server)
    rotaryState.init_ip_menu(noisebox)
    assert rotaryState.__class__.__name__ == "RotaryState_IpPicker_Server"
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
    rotaryState.new_state.assert_called_with(rs.RotaryState_AdvancedSettingsMenu)

    rotaryState.ip_address = ""
    rotaryState.counter = 0
    rotaryState.new_state = new_state_mock

    for click in maximum_clicks:
        rotaryState.counter = click
        rotaryState.switchCallback(noisebox)
    assert rotaryState.ip_address == "173.421.381.222"
    rotaryState.new_state.assert_called_with(rs.RotaryState_AdvancedSettingsMenu)
