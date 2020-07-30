class SwitchState:
    def __init__(self):
        self.new_state(SwitchState_A)

    def new_state(self, state):
        self.__class__ = state

    def action(self):
        print("Action not set")


class SwitchState_A(SwitchState):
    def switchCallback(self, noisebox, oled_menu):

        strval = oled_menu.menu_items[oled_menu.menuindex]

        """check menu value when button clicked and run corresponding function"""
        if (strval == "SERVER 1"):
            print('START JACKTRIP')
            # noisebox.start_jacktrip_session()

        if (strval == "LEVEL METER"):
            print('LEVEL METER')
            # noisebox.start_monitoring_audio()

        if (strval == "CONNECTED PEERS"):
            print('CONNECTED PEERS')
            # noisebox.check_peers()

        if (strval == "IP ADDRESS"):
            print('CONNECTED PEERS')
            #  oled_helpers.draw_text(0, 26, noisebox.get_ip())

        if (strval == "TEST LAYOUT"):
            print('TEST LAYOUT')
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

    def action(self, x):
        print("Do something with", x)
        # revert to state A
        self.new_state(SwitchState_A)
