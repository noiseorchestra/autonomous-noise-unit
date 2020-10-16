from noisebox_helpers import NoiseBoxCustomError, menu, Config


class RotaryState:
    """Base state"""

    def __init__(self, debug=False):
        self.new_state(RotaryState_Menu)
        self.debug = debug
        self.counter = 0
        self.ip_values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", " ->"]
        self.ip_address = ""

    def new_state(self, state):
        self.__class__ = state

    def switchCallback(self, noisebox, oled_menu):
        print("switchCallback not set")

    def rotaryCallback(self, oled_menu, direction):
        print("rotaryCallback not set")

    def drawDefaultMenu(self, oled_menu):
        oled_menu.new_menu_items(oled_menu.default_menu_items)
        self.new_state(RotaryState_Menu)
        oled_menu.draw_menu()

    def ip_picker_attr(self):
        self.counter = 0
        self.ip_values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", " ->"]
        self.ip_address = ""



class RotaryState_Menu(RotaryState):
    """Menu state"""

    def __init__(self, debug=False):
        self.debug = debug

    def switchCallback(self, noisebox, oled_menu, oled):
        """check menu value on button click and run corresponding methods"""

        strval = oled_menu.menu_items[oled_menu.menuindex]

        if (strval == "CONNECT TO SERVER"):
            next_state = RotaryState_JacktripRunning
            try:
                noisebox.start_jacktrip_session()
            except NoiseBoxCustomError as e:
                oled.start_scrolling_text(e.args[0])
                next_state = RotaryState_Scrolling

            if self.debug is True:
                return next_state.__name__
            self.new_state(next_state)

        if (strval == "LEVEL METER"):
            next_state = RotaryState_Monitoring
            try:
                noisebox.start_local_monitoring()
            except NoiseBoxCustomError as e:
                oled.start_scrolling_text(e.args[0])
                next_state = RotaryState_Scrolling

            if self.debug is True:
                return next_state.__name__
            self.new_state(next_state)

        if (strval == "P2P SESSION"):
            next_state = SwitchState_PeersMenu
            oled.draw_text(0, 26, "Searching for peers...")
            online_peers = noisebox.check_peers()
            online_peers.append("START SERVER")
            online_peers.append("<-- BACK")
            oled_menu.new_menu_items(online_peers)

            if self.debug is True:
                return next_state.__name__

            self.new_state(next_state)
            oled_menu.draw_menu()

        if (strval == "SETTINGS -->"):
            next_state = RotaryState_SettingsMenu
            oled_menu.new_menu_items(oled_menu.settings_items)

            if self.debug is True:
                return next_state.__name__

            self.new_state(next_state)
            oled_menu.draw_menu()

    def rotaryCallback(self, oled_menu, direction):
        """Increment menu counter and redraw menu"""

        if direction == 1:
            oled_menu.counter += 1
        else:
            oled_menu.counter -= 1
        oled_menu.draw_menu()


class RotaryState_Monitoring(RotaryState):
    """Monitoring audio state"""

    def switchCallback(self, noisebox, oled_menu, oled):
        noisebox.stop_monitoring()
        self.drawDefaultMenu(oled_menu)

class RotaryState_JacktripRunning(RotaryState):
    """JackTrip running state"""

    def switchCallback(self, noisebox, oled_menu, oled):
        noisebox.stop_jacktrip_session()
        self.drawDefaultMenu(oled_menu)

class RotaryState_JacktripServerWaiting(RotaryState):
    """JackTrip server waiting state"""

    def switchCallback(self, noisebox, oled_menu, oled):
        noisebox.stop_jacktrip_session()
        self.drawDefaultMenu(oled_menu)

class RotaryState_Scrolling(RotaryState):
    """Scrolling oled text state"""

    def switchCallback(self, noisebox, oled_menu, oled):
        oled.stop_scrolling_text()
        self.drawDefaultMenu(oled_menu)

class SwitchState_PeersMenu(RotaryState):
    """New swtitch state"""

    def switchCallback(self, noisebox, oled_menu, oled):
        strval = oled_menu.menu_items[oled_menu.menuindex]

        """check menu value when button clicked and run corresponding function"""
        if (strval == "<-- BACK"):
            self.drawDefaultMenu(oled_menu)

        elif (strval == "START SERVER"):
            try:
                noisebox.start_jacktrip_peer_session(server=True)
                self.new_state(RotaryState_JacktripServerWaiting)
            except NoiseBoxCustomError as e:
                oled.start_scrolling_text(e.args[0])
                self.new_state(RotaryState_Scrolling)
            else:
                self.new_state(RotaryState_JacktripRunning)

        else:
            for menu_item in oled_menu.menu_items:
                if (strval == menu_item):
                    try:
                        noisebox.start_jacktrip_peer_session(server=False, peer_address=menu_item)
                    except NoiseBoxCustomError as e:
                        oled.start_scrolling_text(e.args[0])
                        self.new_state(RotaryState_Scrolling)
                    else:
                        self.new_state(RotaryState_JacktripRunning)

    def rotaryCallback(self, oled_menu, direction):
        if direction == 1:
            oled_menu.counter += 1
        else:
            oled_menu.counter -= 1
        oled_menu.draw_menu()


class RotaryState_SettingsMenu(RotaryState):
    """Settings menu state"""
    def __init__(self, debug=False):
        self.debug = debug

    def switchCallback(self, noisebox, oled_menu, oled):
        """check menu value on button click and run corresponding methods"""

        config = Config()

        if type(oled_menu.menu_items[oled_menu.menuindex]) is dict:
            strval = oled_menu.menu_items[oled_menu.menuindex]["name"]
            value = oled_menu.menu_items[oled_menu.menuindex]["value"]
        else:
            strval = oled_menu.menu_items[oled_menu.menuindex]

        if (strval == "<-- BACK"):
            self.drawDefaultMenu(oled_menu)

        elif (strval == "INPUT"):
            """Toggle input channels mono/stereo"""

            next_input_value = menu.next_input_value(value)
            oled_menu.menu_items[oled_menu.menuindex]["value"] = next_input_value
            if self.debug is True:
                return next_input_value
            config.save(config.change_input_channels(next_input_value))
            oled_menu.draw_menu()

        elif (strval == "JACKTRIP"):
            next_state = RotaryState_AdvancedSettingsMenu
            oled_menu.new_menu_items(oled_menu.advanced_settings_items)

            if self.debug is True:
                return next_state.__name__

            self.new_state(next_state)
            oled_menu.draw_menu()

        elif (strval == "IP ADDRESS"):
            title = ["==HOSTNAME & IP=="]
            oled.draw_lines(title + noisebox.get_ip())
            oled_menu.draw_menu()

        elif (strval == "UPDATE"):
            oled.draw_lines(["==UPDATE==", "Updating system"])
            try:
                noisebox.system_update()
            except NoiseBoxCustomError as e:
                oled.start_scrolling_text(e.args[0])
                self.new_state(RotaryState_Scrolling)

    def rotaryCallback(self, oled_menu, direction):
        """Increment menu counter and redraw menu"""

        if direction == 1:
            oled_menu.counter += 1
        else:
            oled_menu.counter -= 1
        oled_menu.draw_menu()

class RotaryState_AdvancedSettingsMenu(RotaryState):
    """Settings menu state"""
    def __init__(self, debug=False):
        self.debug = debug
        self.counter = 0
        self.ip_values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", " ->"]
        self.ip_address = ""

    def switchCallback(self, noisebox, oled_menu, oled):
        """check menu value on button click and run corresponding methods"""

        config = Config()

        if type(oled_menu.menu_items[oled_menu.menuindex]) is dict:
            strval = oled_menu.menu_items[oled_menu.menuindex]["name"]
            value = oled_menu.menu_items[oled_menu.menuindex]["value"]
        else:
            strval = oled_menu.menu_items[oled_menu.menuindex]

        if (strval == "QUEUE"):
            next_queue_value = menu.next_queue_value(value)
            oled_menu.menu_items[oled_menu.menuindex]["value"] = next_queue_value
            if self.debug is True:
                return next_queue_value
            config.save(config.change_queue(next_queue_value))
            oled_menu.draw_menu()

        if (strval == "CHANNELS"):
            next_channels_value = menu.next_channels_value(value)
            oled_menu.menu_items[oled_menu.menuindex]["value"] = next_channels_value
            if self.debug is True:
                return next_channels_value
            config.save(config.change_output_channels(next_channels_value))
            oled_menu.draw_menu()

        if (strval == "CHANGE IP"):
            oled_menu.counter = 0
            self.new_state(RotaryState_IpPicker)
            oled_menu.draw_ip_menu("0", "" )

        if (strval == "<-- BACK"):
            self.drawDefaultMenu(oled_menu)
            return "<-- BACK"

    def rotaryCallback(self, oled_menu, direction):
        """Increment menu counter and redraw menu"""

        if direction == 1:
            oled_menu.counter += 1
        else:
            oled_menu.counter -= 1
        oled_menu.draw_menu()


class RotaryState_IpPicker(RotaryState):
    """Change IP address"""
    def __init__(self, ip="", debug=False):
        self.debug = debug
        self.config = Config()
        self.counter = 0
        self.ip_values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "<-", " ->"]
        self.ip_address = self.config.get_config()["jacktrip-default"]["ip"]

    def switchCallback(self, noisebox, oled_menu, oled):

        next_string = self.ip_address + self.ip_values[self.counter]

        if self.ip_values[self.counter] is self.ip_values[-1]:
            self.save_ip()
            self.advanced_menu(oled_menu)

        elif self.ip_values[self.counter] is self.ip_values[-2]:
            self.ip_address = self.ip_address[:-1]
            self.counter = 0
            oled_menu.draw_ip_menu(self.ip_values[self.counter], self.ip_address)

        elif len(next_string) == 15:
            self.ip_address = next_string
            self.save_ip()
            self.advanced_menu(oled_menu)

        else:
            self.ip_address += self.ip_values[self.counter]
            self.counter = 0
            oled_menu.draw_ip_menu(self.ip_values[self.counter], self.ip_address)

    def rotaryCallback(self, oled_menu, direction):
        """Increment menu counter and redraw menu"""

        if direction == 1:
            self.counter += 1
        else:
            self.counter -= 1
        oled_menu.draw_ip_menu(self.ip_values[self.counter], self.ip_address)

    def save_ip(self):
        config = Config()
        next_config = config.change_server_ip(self.ip_address)
        if self.debug is True:
            return
        config.save(next_config)

    def advanced_menu(self, oled_menu):
        oled_menu.new_menu_items(oled_menu.advanced_settings_items)
        self.new_state(RotaryState_AdvancedSettingsMenu)
        oled_menu.draw_menu()
