import noisebox_rotary_helpers.rotary_state_actions as actions

class RotaryState:
    """Base state"""

    def __init__(self, debug=False):
        self.debug = debug
        self.new_state(RotaryState_Menu)

    def new_state(self, state):
        self.__class__ = state

    def switchCallback(self, noisebox):
        print("switchCallback not set")

    def rotaryCallback(self, noisebox, direction):
        """Increment menu counter and redraw menu"""

        if direction == 1:
            noisebox.menu.counter += 1
        else:
            noisebox.menu.counter -= 1
        noisebox.menu.draw_menu()

    def get_strval(self, noisebox):
        strval = noisebox.menu.active_menu_items[noisebox.menu.menuindex]
        if type(noisebox.menu.active_menu_items[noisebox.menu.menuindex]) is dict:
            strval = noisebox.menu.active_menu_items[noisebox.menu.menuindex]["name"]
        return strval

    def get_value(self, noisebox):
        value = None
        if type(noisebox.menu.active_menu_items[noisebox.menu.menuindex]) is dict:
            value = noisebox.menu.active_menu_items[noisebox.menu.menuindex]["value"]
        return value

class RotaryState_Menu(RotaryState):
    """Menu state"""

    def __init__(self, debug=False):
        self.debug = debug

    def switchCallback(self, noisebox):
        """check menu value on button click and run corresponding methods"""

        strval = self.get_strval(noisebox)

        if (strval == "CONNECT"):
            self.new_state(actions.start_jacktrip_session(noisebox))

        if (strval == "LEVEL METER"):
            self.new_state(actions.level_meter(noisebox))

        if (strval == "SETTINGS"):
            self.new_state(actions.settings_menu(noisebox))



class RotaryState_Monitoring(RotaryState):
    """Monitoring audio state"""

    def switchCallback(self, noisebox):
        noisebox.stop_monitoring()
        self.new_state(actions.draw_default_menu(noisebox))

    def rotaryCallback(self, noisebox, direction):
        pass

class RotaryState_JacktripRunning(RotaryState):
    """JackTrip running state"""

    def switchCallback(self, noisebox):
        noisebox.stop_jacktrip_session()
        self.new_state(actions.draw_default_menu(noisebox))

    def rotaryCallback(self, noisebox, direction):
        pass

class RotaryState_JacktripServerWaiting(RotaryState):
    """JackTrip server waiting state"""

    def switchCallback(self, noisebox):
        noisebox.stop_jacktrip_session()
        self.new_state(actions.draw_default_menu(noisebox))

    def rotaryCallback(self, noisebox, direction):
        pass

class RotaryState_Scrolling(RotaryState):
    """Scrolling oled text state"""

    def switchCallback(self, noisebox):
        noisebox.oled.stop_scrolling_text()
        self.new_state(actions.draw_default_menu(noisebox))

    def rotaryCallback(self, noisebox, direction):
        pass

class RotaryState_Show(RotaryState):
    """Scrolling oled text state"""

    def switchCallback(self, noisebox):
        self.new_state(actions.draw_settings_menu(noisebox))

    def rotaryCallback(self, noisebox, direction):
        pass

class RotaryState_PeersMenu(RotaryState):
    """New swtitch state"""

    def __init__(self, debug=False):
        self.debug = debug

    def switchCallback(self, noisebox):
        strval = self.get_strval(noisebox)

        if (strval == "<-- BACK"):
            self.new_state(actions.draw_default_menu(noisebox))

        elif (strval == "START SERVER"):
            self.new_state(RotaryState_JacktripServerWaiting)
            self.new_state(actions.start_peer_session_as_server(noisebox))
        else:
            self.new_state(actions.start_peer_session_as_peer(noisebox))



class RotaryState_SettingsMenu(RotaryState):
    """Settings menu state"""
    def __init__(self, debug=False):
        self.debug = debug

    def switchCallback(self, noisebox):
        """check menu value on button click and run corresponding methods"""

        strval = self.get_strval(noisebox)
        value = self.get_value(noisebox)

        if (strval == "<-- BACK"):
            self.new_state(actions.draw_default_menu(noisebox))

        elif (strval == "INPUT"):
            """Toggle input channels mono/stereo"""
            self.new_state(actions.toggle_input_channels(noisebox, value))

        elif (strval == "ADVANCED OPTIONS"):
            self.new_state(actions.jacktrip_menu(noisebox))

        elif (strval == "DEVICE INFO"):
            self.new_state(actions.show_ip_address(noisebox))

        elif (strval == "UPDATE"):
            self.new_state(actions.update(noisebox))


class RotaryState_AdvancedSettingsMenu(RotaryState):
    """Settings menu state"""
    def __init__(self, debug=False):
        self.debug = debug

    def switchCallback(self, noisebox):
        """check menu value on button click and run corresponding methods"""

        strval = self.get_strval(noisebox)
        value = self.get_value(noisebox)

        if (strval == "QUEUE"):
            self.new_state(actions.change_queue(noisebox, value))
        if (strval == "CHANNELS"):
            self.new_state(actions.change_jacktrip_channels(noisebox, value))
        if (strval == "IP"):
            self.new_state(RotaryState_IpPicker_Server)
            self.init_ip_menu(noisebox)
        if (strval == "PPS"):
            self.new_state(actions.change_jack_pps(noisebox, value))
        if (strval == "MODE"):
            self.new_state(actions.change_jacktrip_mode(noisebox, value))
        if (strval == "PEER"):
            self.new_state(RotaryState_IpPicker_Peer)
            self.init_ip_menu(noisebox)
        if (strval == "<-- BACK"):
            self.new_state(actions.exit_advanced_menu(noisebox))
            return "<-- BACK"



class RotaryState_IpPicker(RotaryState):
    """Change IP address"""
    def __init__(self, debug=False):
        super().__init__(self)
        self.debug = debug

    def switchCallback(self, noisebox):

        next_string = self.ip_address + self.ip_values[self.counter]

        if self.ip_values[self.counter] is self.ip_values[-1]:
            self.save_ip(noisebox)
            self.new_state(actions.draw_advanced_menu(noisebox))

        elif self.ip_values[self.counter] is self.ip_values[-2]:
            self.ip_address = self.ip_address[:-1]
            self.counter = -2
            noisebox.menu.draw_ip_menu(self.ip_values[self.counter], self.ip_address)

        elif len(next_string) == 15:
            self.ip_address = next_string
            self.save_ip(noisebox)
            self.new_state(actions.draw_advanced_menu(noisebox))

        else:
            self.ip_address += self.ip_values[self.counter]
            self.counter = -1
            noisebox.menu.draw_ip_menu(self.ip_values[self.counter], self.ip_address)

    def rotaryCallback(self, noisebox, direction):
        """Increment menu counter and redraw menu"""

        if direction == 1:
            self.counter += 1
        else:
            self.counter -= 1
        noisebox.menu.draw_ip_menu(self.ip_values[self.counter], self.ip_address)

class RotaryState_IpPicker_Server(RotaryState_IpPicker):
    """Change IP address"""
    def __init__(self, debug=False):
        super().__init__(self)
        self.debug = debug

    def init_ip_menu(self, noisebox):
        self.noisebox = noisebox
        self.counter = -1
        self.ip_values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "<-", " ->"]
        self.ip_address = self.noisebox.config.get_config()["jacktrip-default"]["ip"]
        self.noisebox.menu.draw_ip_menu(self.ip_values[self.counter], self.ip_address )


    def save_ip(self, noisebox):
        next_config = noisebox.config.change_server_ip(self.ip_address)
        if self.debug is True:
            return
        noisebox.config.save(next_config)

class RotaryState_IpPicker_Peer(RotaryState_IpPicker):
    """Change IP address"""
    def __init__(self, debug=False):
        super().__init__(self)
        self.debug = debug

    def init_ip_menu(self, noisebox):
        self.noisebox = noisebox
        self.counter = -1
        self.ip_values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "<-", " ->"]
        self.ip_address = self.noisebox.config.get_config()["jacktrip-default"]["peer-ip"]
        self.noisebox.menu.draw_ip_menu(self.ip_values[self.counter], self.ip_address )

    def save_ip(self, noisebox):
        next_config = noisebox.config.change_peer_ip(self.ip_address)
        if self.debug is True:
            return
        noisebox.config.save(next_config)
