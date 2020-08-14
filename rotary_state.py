from custom_exceptions import NoiseBoxCustomError

class SwitchState:
    def __init__(self):
        self.new_state(SwitchState_A)

    def new_state(self, state):
        self.__class__ = state

    def switchCallback(self, noisebox, oled_menu):
        print("switchCallback not set")

    def rotaryCallback(self, oled_menu, direction):
        print("Do nothing")


class SwitchState_A(SwitchState):

    def switchCallback(self, noisebox, oled_menu, oled):
        strval = oled_menu.menu_items[oled_menu.menuindex]

        """check menu value when button clicked and run corresponding function"""
        if (strval == "START JACKTRIP"):
            try:
                noisebox.start_jacktrip_session()
            except NoiseBoxCustomError as e:
                oled.start_layout(e.args[0])
                self.new_state(SwitchState_D)
            else:
                self.new_state(SwitchState_C)

        if (strval == "LEVEL METER"):
            try:
                noisebox.start_monitoring_audio()
            except NoiseBoxCustomError as e:
                oled.start_layout(e.args[0])
                self.new_state(SwitchState_D)
            else:
                self.new_state(SwitchState_B)

        if (strval == "CONNECTED PEERS"):
            oled.draw_text(0, 26, "Searching for peers...")
            online_peers = noisebox.check_peers()
            oled.draw_lines(online_peers)

        if (strval == "IP ADDRESS"):
            title = ["==HOSTNAME & IP=="]
            oled.draw_lines(title + noisebox.get_ip())

    def rotaryCallback(self, oled_menu, direction):
        if direction == 1:
            oled_menu.counter += 1
        else:
            oled_menu.counter -= 1
        oled_menu.draw_menu()


class SwitchState_B(SwitchState):
    """New swtitch state"""

    def switchCallback(self, noisebox, oled_menu, oled):
        print('STOP MONITORING')
        noisebox.stop_monitoring_audio()
        self.new_state(SwitchState_A)
        oled_menu.draw_menu()

class SwitchState_C(SwitchState):
    """New swtitch state"""

    def switchCallback(self, noisebox, oled_menu, oled):
        print('STOP JACKTRIP SESSION')
        noisebox.stop_jacktrip_session()
        self.new_state(SwitchState_A)
        oled_menu.draw_menu()

class SwitchState_D(SwitchState):
    """New swtitch state"""

    def switchCallback(self, noisebox, oled_menu, oled):
        print('STOP LAYOUT')
        oled.stop_layout()
        self.new_state(SwitchState_A)
        oled_menu.draw_menu()
