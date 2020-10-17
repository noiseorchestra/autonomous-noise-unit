import noisebox_helpers as nh

def connect_to_server(noisebox, success_state, fail_state=None):
    next_state = success_state
    try:
        noisebox.start_jacktrip_session()
    except nh.NoiseBoxCustomError as e:
        noisebox.oled.start_scrolling_text(e.args[0])
        next_state = fail_state
    return next_state

def level_meter(noisebox, success_state, fail_state=None):
    next_state = success_state
    try:
        noisebox.start_local_monitoring()
    except nh.NoiseBoxCustomError as e:
        noisebox.oled.start_scrolling_text(e.args[0])
        next_state = fail_state
    return next_state

def p2p_session(noisebox, success_state, fail_state=None):
    noisebox.oled.draw_text(0, 26, "Searching for peers...")
    online_peers = noisebox.check_peers()
    online_peers.append("START SERVER")
    online_peers.append("<-- BACK")
    noisebox.menu.new_menu_items(online_peers)
    return success_state

def settings_menu(noisebox, success_state, fail_state=None):
    settings_items = noisebox.menu.get_settings_items(noisebox.config)
    noisebox.menu.new_menu_items(settings_items)
    return success_state

# def start_peer_session_as_server():
#     try:
#         noisebox.start_jacktrip_peer_session(server=True)
#         self.new_state(RotaryState_JacktripServerWaiting)
#     except nh.NoiseBoxCustomError as e:
#         noisebox.oled.start_scrolling_text(e.args[0])
#         self.new_state(RotaryState_Scrolling)
#     else:
#         self.new_state(RotaryState_JacktripRunning)
