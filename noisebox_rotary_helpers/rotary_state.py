import noisebox_helpers as nh
from noisebox_rotary_helpers.rotary_state_actions import RotaryStateActions

ip_values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "<-", " ->"]

class RotaryState:
    """Base state"""

    def __init__(self):
        self.debug = False
        self.new_state(RotaryState_Menu)

    def new_state(self, state):
        self.__class__ = state

    def switchCallback(self, noisebox):
        print("switchCallback not set")

    def rotaryCallback(self, noisebox, direction):
        print("rotaryCallback not set")

    def drawDefaultMenu(self, noisebox):
        noisebox.menu.new_menu_items(noisebox.menu.default_menu_items)
        self.new_state(RotaryState_Menu)
        noisebox.menu.draw_menu()


class RotaryState_Menu(RotaryState):
    """Menu state"""

    def __init__(self, debug=False):
        self.debug = debug

    def switchCallback(self, noisebox):
        """check menu value on button click and run corresponding methods"""

        strval = noisebox.menu.menu_items[noisebox.menu.menuindex]
        actions = RotaryStateActions(noisebox)

        if (strval == "CONNECT TO SERVER"):
            self.new_state(actions.connect_to_server(RotaryState_JacktripRunning, RotaryState_Scrolling))

        if (strval == "LEVEL METER"):
            self.new_state(actions.level_meter(RotaryState_Monitoring, RotaryState_Scrolling))

        if (strval == "P2P SESSION"):
            self.new_state(actions.p2p_session(SwitchState_PeersMenu))
            noisebox.menu.draw_menu()

        if (strval == "SETTINGS -->"):
            self.new_state(actions.settings_menu(RotaryState_SettingsMenu))
            noisebox.menu.draw_menu()

    def rotaryCallback(self, noisebox, direction):
        """Increment menu counter and redraw menu"""

        if direction == 1:
            noisebox.menu.counter += 1
        else:
            noisebox.menu.counter -= 1
        noisebox.menu.draw_menu()


class RotaryState_Monitoring(RotaryState):
    """Monitoring audio state"""

    def switchCallback(self, noisebox):
        noisebox.stop_monitoring()
        self.drawDefaultMenu(noisebox)

class RotaryState_JacktripRunning(RotaryState):
    """JackTrip running state"""

    def switchCallback(self, noisebox):
        noisebox.stop_jacktrip_session()
        self.drawDefaultMenu(noisebox)

class RotaryState_JacktripServerWaiting(RotaryState):
    """JackTrip server waiting state"""

    def switchCallback(self, noisebox):
        noisebox.stop_jacktrip_session()
        self.drawDefaultMenu(noisebox)

class RotaryState_Scrolling(RotaryState):
    """Scrolling oled text state"""

    def switchCallback(self, noisebox):
        noisebox.oled.stop_scrolling_text()
        self.drawDefaultMenu(noisebox)

class SwitchState_PeersMenu(RotaryState):
    """New swtitch state"""

    def switchCallback(self, noisebox):
        strval = noisebox.menu.menu_items[noisebox.menu.menuindex]

        """check menu value when button clicked and run corresponding function"""
        if (strval == "<-- BACK"):
            self.drawDefaultMenu(noisebox)

        elif (strval == "START SERVER"):
            try:
                noisebox.start_jacktrip_peer_session(server=True)
                self.new_state(RotaryState_JacktripServerWaiting)
            except nh.NoiseBoxCustomError as e:
                noisebox.oled.start_scrolling_text(e.args[0])
                self.new_state(RotaryState_Scrolling)
            else:
                self.new_state(RotaryState_JacktripRunning)

        else:
            for menu_item in noisebox.menu.menu_items:
                if (strval == menu_item):
                    try:
                        noisebox.start_jacktrip_peer_session(server=False, peer_address=menu_item)
                    except nh.NoiseBoxCustomError as e:
                        noisebox.oled.start_scrolling_text(e.args[0])
                        self.new_state(RotaryState_Scrolling)
                    else:
                        self.new_state(RotaryState_JacktripRunning)

    def rotaryCallback(self, noisebox, direction):
        if direction == 1:
            noisebox.menu.counter += 1
        else:
            noisebox.menu.counter -= 1
        noisebox.menu.draw_menu()


class RotaryState_SettingsMenu(RotaryState):
    """Settings menu state"""
    def __init__(self, debug=False):
        self.debug = debug

    def switchCallback(self, noisebox):
        """check menu value on button click and run corresponding methods"""

        if type(noisebox.menu.menu_items[noisebox.menu.menuindex]) is dict:
            strval = noisebox.menu.menu_items[noisebox.menu.menuindex]["name"]
            value = noisebox.menu.menu_items[noisebox.menu.menuindex]["value"]
        else:
            strval = noisebox.menu.menu_items[noisebox.menu.menuindex]

        if (strval == "<-- BACK"):
            self.drawDefaultMenu(noisebox)

        elif (strval == "INPUT"):
            """Toggle input channels mono/stereo"""

            next_input_value = noisebox.menu.next_input_value(value)
            noisebox.menu.menu_items[noisebox.menu.menuindex]["value"] = next_input_value
            if self.debug is True:
                return next_input_value
            noisebox.config.save(noisebox.config.change_input_channels(next_input_value))
            noisebox.menu.draw_menu()

        elif (strval == "JACKTRIP"):
            next_state = RotaryState_AdvancedSettingsMenu
            noisebox.menu.new_menu_items(noisebox.menu.get_advanced_settings_items(noisebox.config))

            if self.debug is True:
                return next_state.__name__

            self.new_state(next_state)
            noisebox.menu.draw_menu()

        elif (strval == "IP ADDRESS"):
            title = ["==HOSTNAME & IP=="]
            noisebox.oled.draw_lines(title + noisebox.get_ip())
            noisebox.menu.draw_menu()

        elif (strval == "UPDATE"):
            noisebox.oled.draw_lines(["==UPDATE==", "Updating system"])
            try:
                noisebox.system_update()
            except nh.NoiseBoxCustomError as e:
                noisebox.oled.start_scrolling_text(e.args[0])
                self.new_state(RotaryState_Scrolling)

    def rotaryCallback(self, noisebox, direction):
        """Increment menu counter and redraw menu"""

        if direction == 1:
            noisebox.menu.counter += 1
        else:
            noisebox.menu.counter -= 1
        noisebox.menu.draw_menu()

class RotaryState_AdvancedSettingsMenu(RotaryState):
    """Settings menu state"""
    def __init__(self, debug=False):
        self.debug = debug

    def switchCallback(self, noisebox):
        """check menu value on button click and run corresponding methods"""

        config = nh.Config()

        if type(noisebox.menu.menu_items[noisebox.menu.menuindex]) is dict:
            strval = noisebox.menu.menu_items[noisebox.menu.menuindex]["name"]
            value = noisebox.menu.menu_items[noisebox.menu.menuindex]["value"]
        else:
            strval = noisebox.menu.menu_items[noisebox.menu.menuindex]

        if (strval == "QUEUE"):
            next_queue_value = noisebox.menu.next_queue_value(value)
            noisebox.menu.menu_items[noisebox.menu.menuindex]["value"] = next_queue_value
            if self.debug is True:
                return next_queue_value
            noisebox.config.save(noisebox.config.change_queue(next_queue_value))
            noisebox.menu.draw_menu()

        if (strval == "CHANNELS"):
            next_channels_value = noisebox.menu.next_channels_value(value)
            noisebox.menu.menu_items[noisebox.menu.menuindex]["value"] = next_channels_value
            if self.debug is True:
                return next_channels_value
            noisebox.config.save(noisebox.config.change_output_channels(next_channels_value))
            noisebox.menu.draw_menu()

        if (strval == "IP"):
            self.new_state(RotaryState_IpPicker)
            self.counter = -1
            self.ip_values = ip_values
            self.ip_address = noisebox.config.get_config()["jacktrip-default"]["ip"]
            noisebox.menu.draw_ip_menu(self.ip_values[self.counter], self.ip_address )

        if (strval == "<-- BACK"):
            self.drawDefaultMenu(noisebox)
            return "<-- BACK"

    def rotaryCallback(self, noisebox, direction):
        """Increment menu counter and redraw menu"""

        if direction == 1:
            noisebox.menu.counter += 1
        else:
            noisebox.menu.counter -= 1
        noisebox.menu.draw_menu()


class RotaryState_IpPicker(RotaryState):
    """Change IP address"""
    def __init__(self, debug=False):
        self.debug = debug
        self.counter = -1
        self.ip_values = ip_values
        self.ip_address = "111.111.111.111"

    def switchCallback(self, noisebox):

        next_string = self.ip_address + self.ip_values[self.counter]

        if self.ip_values[self.counter] is self.ip_values[-1]:
            self.save_ip(noisebox)
            self.advanced_menu(noisebox)

        elif self.ip_values[self.counter] is self.ip_values[-2]:
            self.ip_address = self.ip_address[:-1]
            self.counter = -2
            noisebox.menu.draw_ip_menu(self.ip_values[self.counter], self.ip_address)

        elif len(next_string) == 15:
            self.ip_address = next_string
            self.save_ip(noisebox)
            self.advanced_menu(noisebox)

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

    def save_ip(self, noisebox):
        next_config = noisebox.config.change_server_ip(self.ip_address)
        if self.debug is True:
            return
        noisebox.config.save(next_config)

    def advanced_menu(self, noisebox):
        noisebox.menu.new_menu_items(noisebox.menu.get_advanced_settings_items(noisebox.config))
        self.new_state(RotaryState_AdvancedSettingsMenu)
        noisebox.menu.draw_menu()
