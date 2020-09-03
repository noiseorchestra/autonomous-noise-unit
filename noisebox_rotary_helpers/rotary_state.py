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

    def drawDefaultMenu(self, oled_menu):
        oled_menu.new_menu_items(oled_menu.default_menu_items)
        self.new_state(RotaryState_Menu)
        oled_menu.draw_menu()



class RotaryState_Menu(RotaryState):
    """Menu state"""

    def __init__(self):
        self.new_state(RotaryState_Menu)

    def switchCallback(self, noisebox, oled_menu, oled):
        """check menu value on button click and run corresponding methods"""

        strval = oled_menu.menu_items[oled_menu.menuindex]

        if (strval == "CONNECT TO SERVER"):
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

        if (strval == "P2P SESSION"):
            oled.draw_text(0, 26, "Searching for peers...")
            online_peers = noisebox.check_peers()
            online_peers.append("START SERVER")
            online_peers.append("<-- BACK")
            oled_menu.new_menu_items(online_peers)
            self.new_state(SwitchState_PeersMenu)
            oled_menu.draw_menu()

        if (strval == "SETTINGS -->"):
            oled_menu.new_menu_items(["MONO INPUT", "MONO JACKTRIP", "IP ADDRESS", "<-- BACK"])
            self.new_state(RotaryState_SettingsMenu)
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

    def switchCallback(self, noisebox, oled_menu, oled):
        """check menu value on button click and run corresponding methods"""

        strval = oled_menu.menu_items[oled_menu.menuindex]

        if (strval == "<-- BACK"):
            self.drawDefaultMenu(oled_menu)

        elif (strval == "MONO INPUT"):
            """Toggle input channels mono/stereo"""

            next_ch = "1" if noisebox.session_params['input-channels'] == "2" else "2"
            noisebox.session_params['input-channels'] = next_ch
            noisebox.save_settings()
            oled_menu.toggle_selected_items(["MONO INPUT"])
            oled.draw_lines(["==INPUT==", "Channels: " +  next_ch])
            self.drawDefaultMenu(oled_menu)

        elif (strval == "MONO JACKTRIP"):
            """Toggle jacktrip channels mono/stereo"""

            next_ch = "1" if noisebox.session_params['jacktrip-channels'] == "2" else "2"
            noisebox.session_params['jacktrip-channels'] = next_ch
            noisebox.save_settings()
            oled_menu.toggle_selected_items(["MONO JACKTRIP"])
            oled.draw_lines(["==JACKTRIP==", "Channels: " +  next_ch])
            self.drawDefaultMenu(oled_menu)

        elif (strval == "SERVER A"):
            """Select server A"""

            ip = noisebox.config.get('server1', 'ip')
            oled_menu.toggle_selected_items(["SERVER A", "SERVER B"])
            oled.draw_lines(["==SERVER==", "ip: " +  ip])
            self.drawDefaultMenu(oled_menu)

        elif (strval == "IP ADDRESS"):
            title = ["==HOSTNAME & IP=="]
            oled.draw_lines(title + noisebox.get_ip())
            oled_menu.new_menu_items(oled_menu.default_menu_items)
            self.new_state(RotaryState_Menu)

    def rotaryCallback(self, oled_menu, direction):
        """Increment menu counter and redraw menu"""

        if direction == 1:
            oled_menu.counter += 1
        else:
            oled_menu.counter -= 1
        oled_menu.draw_menu()
