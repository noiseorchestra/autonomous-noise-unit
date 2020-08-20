#!/usr/bin/python3

import RPi.GPIO as GPIO
import configparser as cp
from time import sleep
import noisebox_rotary_helpers
import noisebox_oled
import noisebox_oled_helpers
import noisebox_helpers as nh

cfg = cp.ConfigParser(interpolation=cp.ExtendedInterpolation())
cfg.read('config.ini')


class Noisebox:
    """Main noisebox object"""

    def __init__(self, jack_helper, oled):
        self.current_server = cfg.get('jacktrip-default', 'ip')
        self.peers = cfg.get('peers', 'ips').split(',')
        self.online_peers = None
        self.session_params = {
            'hub_mode': cfg.get('jacktrip-default', 'hub_mode'),
            'server': cfg.get('jacktrip-default', 'server'),
            'ip': cfg.get('jacktrip-default', 'ip'),
            'channels': cfg.get('jacktrip-default', 'channels'),
            'queue': cfg.get('jacktrip-default', 'queue')
            }
        self.pytrip = nh.PyTrip()
        self.oled = oled
        self.jack_helper = jack_helper
        self.pytrip_watch = nh.PyTripWatch()
        self.pytrip_wait = nh.PyTripWait()


    def get_ip(self):
        """Get and return ip"""

        result = nh.ip_address()

        return result

    def check_peers(self):
        """Check status of all peers and show results"""

        checkPeers = nh.CheckPeers()
        self.online_peers = checkPeers.run(self.peers)

        return self.online_peers

    def start_monitoring_audio(self):
        """Start monitoring audio"""
        self.start_level_meters()
        self.jack_helper.make_monitoring_connections()

    def start_level_meters(self):
        try:
            port_names = self.jack_helper.get_input_port_names()
        except nh.NoiseBoxCustomError:
            raise
        else:
            self.level_meters = [nh.LevelMeter(port) for port in port_names]
            self.oled.start_meters(self.level_meters)

    def start_jacktrip_session(self):
        """Start hubserver JackTrip session"""

        try:
            self.oled.draw_lines(["==START JACKTRIP==", "Connecting to:", self.current_server])
            self.pytrip.start(self.session_params)
        except Exception:
            self.oled.draw_lines(["==JACKTRIP ERROR==", "JackTrip failed to start"])
            self.pytrip.stop()
            raise
        else:
            self.jack_helper.disconnect_session()
            self.pytrip_watch.run(self.pytrip)
            self.pytrip_wait.run(self.pytrip_watch, self.current_server)
            message = self.pytrip_wait.message

            if self.pytrip_wait.connected:
                print("JACKTRIP CONNECTED")
                self.oled.draw_lines(message)
                self.start_level_meters()
                self.jack_helper.make_jacktrip_connections(self.current_server)
            else:
                print("JACKTRIP NOT CONNECTED")
                self.oled.draw_lines(message)
                self.pytrip_watch.terminate()
                raise nh.NoiseBoxCustomError(message)

    def stop_monitoring_audio(self):
        """Stop monitoring audio"""

        self.oled.stop_meters()
        for thread in self.level_meters:
            thread.terminate()
        self.jack_helper.disconnect_session()

    def stop_jacktrip_session(self):
        """Stop JackTrip session"""

        self.stop_monitoring_audio()
        self.pytrip.stop()
        self.oled.draw_text(0, 26, "JackTrip stopped")
        sleep(1)


def main():

    menu_items = ['START JACKTRIP',
                  'LEVEL METER',
                  'CONNECTED PEERS',
                  'IP ADDRESS']

    oled = noisebox_oled.OLED()
    jack_helper = nh.JackHelper(oled)
    jack_helper.start()

    receive_ports = jack_helper.jackClient.get_ports(is_audio=True, is_output=True)
    for port in receive_ports:
        jack_helper.disconnect_all(port)

    oled_menu = noisebox_oled_helpers.Menu(menu_items)

    noisebox = Noisebox(jack_helper, oled)

    ky040 = noisebox_rotary_helpers.KY040(noisebox, oled_menu)
    ky040.start()

    oled_menu.start(noisebox.oled.device)

    try:
        while True:
            sleep(0.1)
    finally:
        ky040.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    main()
