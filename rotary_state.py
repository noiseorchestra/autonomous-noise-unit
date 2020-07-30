from oled_helpers import OLED_helpers

class SwitchState:
    def __init__(self):
        self.new_state(SwitchState_A)

    def new_state(self, state):
        self.__class__ = state

    def switchCallback(self, noisebox, oled_menu):
        print("switchCallback not set")

    def rotaryCallback(self, oled_menu, direction):
        print("rotaryCallback not set")


class SwitchState_A(SwitchState):

    def switchCallback(self, noisebox, oled_menu, oled_helpers):
        strval = oled_menu.menu_items[oled_menu.menuindex]

        """check menu value when button clicked and run corresponding function"""
        if (strval == "START JACKTRIP"):
            try:
                noisebox.start_jacktrip_session()
                self.new_state(SwitchState_C)
            except Exception as e:
                oled_helpers.draw_lines(e.args[0])

        if (strval == "LEVEL METER"):
            try:
                noisebox.start_monitoring_audio()
                self.new_state(SwitchState_B)
            except Exception as e:
                oled_helpers.draw_text(0, 26, e.args[0])

        if (strval == "CONNECTED PEERS"):
            oled_helpers.draw_text(0, 26, "Searching for peers...")
            online_peers = noisebox.check_peers()
            oled_helpers.draw_lines(online_peers)

        if (strval == "IP ADDRESS"):
            oled_helpers.draw_text(0, 26, noisebox.get_ip())

        # if (strval == "TEST LAYOUT"):
            # layout = oled_layout.Layout()
            # layout.render(self.oled_helpers.get_device())

    def rotaryCallback(self, oled_menu, direction):
        if direction == 1:
            oled_menu.counter += 1
        else:
            oled_menu.counter -= 1
        oled_menu.draw_menu()


class SwitchState_B(SwitchState):
    """New swtitch state"""

    def switchCallback(self, noisebox, oled_menu, oled_helpers):
        print('STOP MONITORING')
        noisebox.stop_monitoring_audio()
        self.new_state(SwitchState_A)

    def rotaryCallback(self, oled_menu, direction):
        print("Do nothing")


class SwitchState_C(SwitchState):
    """New swtitch state"""

    def switchCallback(self, noisebox, oled_menu, oled_helpers):
        print('STOP JACKTRIP SESSION')
        noisebox.stop_jacktrip_session()
        self.new_state(SwitchState_A)

    def rotaryCallback(self, oled_menu, direction):
        print("Do nothing")
