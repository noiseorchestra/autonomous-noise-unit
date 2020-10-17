import noisebox_helpers as nh

class RotaryStateActions:
    def __init__(self, noisebox):
        self.noisebox = noisebox

    def connect_to_server(self, success_state, fail_state=None):
        next_state = success_state
        try:
            self.noisebox.start_jacktrip_session()
        except nh.NoiseBoxCustomError as e:
            self.noisebox.oled.start_scrolling_text(e.args[0])
            next_state = fail_state
        return next_state

    def level_meter(self, success_state, fail_state=None):
        next_state = success_state
        try:
            self.noisebox.start_local_monitoring()
        except nh.NoiseBoxCustomError as e:
            self.noisebox.oled.start_scrolling_text(e.args[0])
            next_state = fail_state
        return next_state

    def p2p_session(self, success_state, fail_state=None):
        self.noisebox.oled.draw_text(0, 26, "Searching for peers...")
        online_peers = self.noisebox.check_peers()
        online_peers.append("START SERVER")
        online_peers.append("<-- BACK")
        self.noisebox.menu.new_menu_items(online_peers)
        return success_state

    def settings_menu(self, success_state, fail_state=None):
        self.noisebox.menu.new_menu_items(nh.menu.get_settings_items(self.noisebox.config))
        return success_state
