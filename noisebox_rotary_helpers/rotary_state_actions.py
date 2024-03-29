import noisebox_helpers as nh
import noisebox_rotary_helpers.rotary_state as rs

def connect_to_server(noisebox):
    next_state = rs.RotaryState_JacktripRunning
    try:
        noisebox.start_jacktrip_session()
    except nh.NoiseBoxCustomError as e:
        noisebox.oled.start_scrolling_text(e.args[0])
        next_state = rs.RotaryState_Scrolling
    return next_state

def level_meter(noisebox):
    next_state = rs.RotaryState_Monitoring
    try:
        noisebox.start_local_monitoring()
    except nh.NoiseBoxCustomError as e:
        noisebox.oled.start_scrolling_text(e.args[0])
        next_state = rs.RotaryState_Scrolling
    return next_state

def p2p_session(noisebox):
    noisebox.oled.draw_text(0, 26, "Searching for peers...")
    online_peers = noisebox.check_peers()
    online_peers.append("START SERVER")
    online_peers.append("<-- BACK")
    noisebox.menu.reset_menu()
    noisebox.menu.set_new_menu_items(online_peers)
    noisebox.menu.draw_menu()
    return rs.RotaryState_PeersMenu

def settings_menu(noisebox):
    settings_items = noisebox.menu.settings_items
    noisebox.menu.reset_menu()
    noisebox.menu.set_settings_menu()
    noisebox.menu.draw_menu()
    return rs.RotaryState_SettingsMenu

def start_jacktrip_session(noisebox):
    if noisebox.get_session_params()["jacktrip-mode"] == "p2p":
        return p2p_session(noisebox)
    else:
        return connect_to_server(noisebox)

def start_peer_session_as_server(noisebox):
    next_state = rs.RotaryState_JacktripRunning
    try:
        noisebox.start_jacktrip_peer_session(server=True)
    except nh.NoiseBoxCustomError as e:
        noisebox.oled.start_scrolling_text(e.args[0])
        next_state = rs.RotaryState_Scrolling
    return next_state

def start_peer_session_as_peer(noisebox):
    strval = noisebox.menu.active_menu_items[noisebox.menu.menuindex]
    next_state = rs.RotaryState_JacktripRunning
    for menu_item in noisebox.menu.active_menu_items:
        if (strval == menu_item):
            try:
                noisebox.start_jacktrip_peer_session(server=False, peer_address=menu_item)
            except nh.NoiseBoxCustomError as e:
                noisebox.oled.start_scrolling_text(e.args[0])
                next_state = rs.RotaryState_Scrolling
            return next_state

def toggle_input_channels(noisebox, value):
    next_input_value = noisebox.menu.next_input_value()
    noisebox.config.save(noisebox.config.change_input_channels(next_input_value))
    noisebox.menu.reset_menu()
    noisebox.menu.set_settings_menu()
    noisebox.menu.draw_menu()
    return rs.RotaryState_SettingsMenu

def jacktrip_menu(noisebox):
    noisebox.menu.reset_menu()
    noisebox.menu.set_advanced_menu()
    noisebox.menu.draw_menu()
    return rs.RotaryState_AdvancedSettingsMenu

def show_ip_address(noisebox):
    title = ["==HOSTNAME & IP=="]
    noisebox.oled.start_scrolling_text(title + noisebox.get_ip())
    return rs.RotaryState_Scrolling

def update(noisebox):
    noisebox.oled.draw_lines(["==UPDATE==", "Updating system"])
    try:
        noisebox.system_update()
    except nh.NoiseBoxCustomError as e:
        noisebox.oled.start_scrolling_text(e.args[0])
        return rs.RotaryState_Scrolling
    return rs.RotaryState_Menu

def shutdown(noisebox):
    noisebox.oled.draw_lines(["==SHUTTING DOWN==", "wait 5 seconds", "then unplug your ANU"])
    try:
        noisebox.shutdown()
    except nh.NoiseBoxCustomError as e:
        noisebox.oled.start_scrolling_text(e.args[0])
        return rs.RotaryState_Scrolling
    return rs.RotaryState_Menu

def change_queue(noisebox, value):
    next_queue_value = noisebox.menu.next_queue_value()
    noisebox.config.save(noisebox.config.change_queue(next_queue_value))
    noisebox.menu.set_advanced_menu()
    noisebox.menu.draw_menu()
    return rs.RotaryState_AdvancedSettingsMenu

def change_jacktrip_channels(noisebox, value):
    next_channels_value = noisebox.menu.next_channels_value()
    noisebox.config.save(noisebox.config.change_output_channels(next_channels_value))
    noisebox.menu.set_advanced_menu()
    noisebox.menu.draw_menu()
    return rs.RotaryState_AdvancedSettingsMenu

def change_jack_fpp(noisebox, value):
    next_fpp_value = noisebox.menu.next_fpp_value()
    noisebox.config.save(noisebox.config.change_jack_fpp(next_fpp_value))
    noisebox.menu.set_advanced_menu()
    noisebox.menu.draw_menu()
    return rs.RotaryState_AdvancedSettingsMenu

def change_jacktrip_mode(noisebox, value):
    next_mode_value = noisebox.menu.next_mode_value()
    noisebox.config.save(noisebox.config.change_jacktrip_mode(next_mode_value))
    noisebox.menu.set_advanced_menu()
    noisebox.menu.draw_menu()
    return rs.RotaryState_AdvancedSettingsMenu

def draw_advanced_menu(noisebox):
    noisebox.menu.reset_menu()
    noisebox.menu.set_advanced_menu()
    noisebox.menu.draw_menu()
    return rs.RotaryState_AdvancedSettingsMenu

def draw_default_menu(noisebox):
    noisebox.menu.reset_menu()
    noisebox.menu.set_main_menu()
    noisebox.menu.draw_menu()
    return rs.RotaryState_Menu

def draw_settings_menu(noisebox):
    noisebox.menu.reset_menu()
    noisebox.menu.set_settings_menu()
    noisebox.menu.draw_menu()
    return rs.RotaryState_SettingsMenu

def exit_advanced_menu(noisebox):
    noisebox.restart_jack_if_needed()
    noisebox.menu.reset_menu()
    noisebox.menu.set_main_menu()
    noisebox.menu.draw_menu()
    return rs.RotaryState_Menu
