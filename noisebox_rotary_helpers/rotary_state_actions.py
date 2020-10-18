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
    noisebox.menu.new_menu_items(online_peers)
    return rs.RotaryState_PeersMenu

def settings_menu(noisebox):
    settings_items = noisebox.menu.get_settings_items(noisebox.config)
    noisebox.menu.new_menu_items(settings_items)
    return rs.RotaryState_SettingsMenu

def start_peer_session_as_server(noisebox):
    next_state = rs.RotaryState_JacktripRunning
    try:
        noisebox.start_jacktrip_peer_session(server=True)
    except nh.NoiseBoxCustomError as e:
        noisebox.oled.start_scrolling_text(e.args[0])
        next_state = rs.RotaryState_Scrolling
    return next_state

def start_peer_session_as_peer(noisebox):
    strval = noisebox.menu.menu_items[noisebox.menu.menuindex]
    next_state = rs.RotaryState_JacktripRunning
    for menu_item in noisebox.menu.menu_items:
        if (strval == menu_item):
            try:
                noisebox.start_jacktrip_peer_session(server=False, peer_address=menu_item)
            except nh.NoiseBoxCustomError as e:
                noisebox.oled.start_scrolling_text(e.args[0])
                next_state = rs.RotaryState_Scrolling
            return next_state

def toggle_input_channels(noisebox, value):
    next_input_value = noisebox.menu.next_input_value(value)
    noisebox.menu.menu_items[noisebox.menu.menuindex]["value"] = next_input_value
    noisebox.config.save(noisebox.config.change_input_channels(next_input_value))
    noisebox.menu.draw_menu()

def jacktrip_menu(noisebox):
    noisebox.menu.new_menu_items(noisebox.menu.get_advanced_settings_items(noisebox.config))
    noisebox.menu.draw_menu()
    return rs.RotaryState_AdvancedSettingsMenu

def show_ip_address(noisebox):
    title = ["==HOSTNAME & IP=="]
    noisebox.oled.draw_lines(title + noisebox.get_ip())
    noisebox.menu.draw_menu()

def update(noisebox):
    noisebox.oled.draw_lines(["==UPDATE==", "Updating system"])
    try:
        noisebox.system_update()
    except nh.NoiseBoxCustomError as e:
        noisebox.oled.start_scrolling_text(e.args[0])
        return rs.RotaryState_Scrolling
    return rs.RotaryState_Menu

def change_queue(noisebox, value):
    next_queue_value = noisebox.menu.next_queue_value(value)
    noisebox.menu.menu_items[noisebox.menu.menuindex]["value"] = next_queue_value
    noisebox.config.save(noisebox.config.change_queue(next_queue_value))
    noisebox.menu.draw_menu()
