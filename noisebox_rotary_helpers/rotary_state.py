from noisebox_helpers import NoiseBoxCustomError


class RotaryState:
    """Base state"""

    def __init__(self):
        self.new_state(RotaryState_Menu)

    def new_state(self, state):
        self.__class__ = state

    def switchCallback(self, noisebox, oled_menu):
        print("switchCallback not set")

    def rotaryCallback(self, oled_menu, direction):
        print("rotaryCallback not set")


class RotaryState_Menu(RotaryState):
    """Menu state"""

    def switchCallback(self, noisebox, oled_menu, oled):
        """check menu value on button click and run corresponding methods"""

        strval = oled_menu.menu_items[oled_menu.menuindex]

        if (strval == "START JACKTRIP"):
            try:
                noisebox.start_jacktrip_session()
            except NoiseBoxCustomError as e:
                oled.start_scrolling_text(e.args[0])
                self.new_state(RotaryState_Scrolling)
            else:
                self.new_state(RotaryState_JacktripRunning)

        if (strval == "LEVEL METER"):
            try:
                noisebox.start_local_monitoring()
            except NoiseBoxCustomError as e:
                oled.start_scrolling_text(e.args[0])
                self.new_state(RotaryState_Scrolling)
            else:
                self.new_state(RotaryState_Monitoring)

        if (strval == "CONNECTED PEERS"):
            oled.draw_text(0, 26, "Searching for peers...")
            online_peers = noisebox.check_peers()
            oled.draw_lines(["==ONLINE PEERS=="] + online_peers)

        if (strval == "IP ADDRESS"):
            title = ["==HOSTNAME & IP=="]
            oled.draw_lines(title + noisebox.get_ip())

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
        self.new_state(RotaryState_Menu)
        oled_menu.draw_menu()

class RotaryState_JacktripRunning(RotaryState):
    """JackTrip running state"""

    def switchCallback(self, noisebox, oled_menu, oled):
        noisebox.stop_jacktrip_session()
        self.new_state(RotaryState_Menu)
        oled_menu.draw_menu()

class RotaryState_Scrolling(RotaryState):
    """Scrolling oled text state"""

    def switchCallback(self, noisebox, oled_menu, oled):
        oled.stop_scrolling_text()
        self.new_state(RotaryState_Menu)
        oled_menu.draw_menu()

class SwitchState_P2pJacktripMenu(RotaryState):
    """New swtitch state"""

    def switchCallback(self, noisebox, oled_menu, oled):
        strval = oled_menu.menu_items[oled_menu.menuindex]

        """check menu value when button clicked and run corresponding function"""
        if (strval == "back"):
            print("go back")
            oled_menu.new_menu_items(oled_menu.default_menu_items)
            self.new_state(RotaryState_Menu)

        for menu_item in oled_menu.menu_items:
            if (strval == menu_item):
                print("connect to: ", menu_item)
                try:
                    noisebox.start_jacktrip_peer_session(menu_item)
                except NoiseBoxCustomError as e:
                    oled.start_layout(e.args[0])
                    self.new_state(RotaryState_Scrolling)
                else:
                    oled_menu.new_menu_items(oled_menu.default_menu_items)
                    self.new_state(RotaryState_JacktripRunning)

    def rotaryCallback(self, oled_menu, direction):
        if direction == 1:
            oled_menu.counter += 1
        else:
            oled_menu.counter -= 1
        oled_menu.draw_menu()
