#!/usr/bin/python3

import RPi.GPIO as GPIO
import configparser
from threading import Thread
from time import sleep
import noisebox_rotary_helpers
import noisebox_oled
import noisebox_oled_helpers
import noisebox_helpers

cfg = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
cfg.read('config.ini')
peers = cfg.get('peers', 'ips')
default_jacktrip_params = {
    'hub_mode': cfg.get('jacktrip-default', 'hub_mode'),
    'server': cfg.get('jacktrip-default', 'server'),
    'ip': cfg.get('jacktrip-default', 'ip'),
    'channels': cfg.get('jacktrip-default', 'channels'),
    'queue': cfg.get('jacktrip-default', 'queue')
    }


class Noisebox:
    """Main noisebox object"""

    def __init__(self, jackHelper, oled):
        self.active_server = default_jacktrip_params['ip']
        self.peers = peers.split(',')
        self.online_peers = peers.split(',')
        self.session_params = default_jacktrip_params
        self.current_pytrip = None
        self.oled = oled
        self.jackHelper = jackHelper

    def get_ip(self):
        """Get and return ip"""

        result = noisebox_helpers.ip_address()

        return result

    def check_peers(self):
        """Check status of all peers and show results"""

        checkPeers = noisebox_helpers.CheckPeers()
        self.online_peers = checkPeers.run(self.peers)

        return self.online_peers

    def start_monitoring_audio(self):
        """Start monitoring audio"""
        self.jackHelper.make_monitoring_connections()

    def start_level_meters(self):
        port_names = self.jackHelper.get_input_port_names()
        self.level_meters = [noisebox_helpers.LevelMeter(port) for port in port_names]
        self.oled.start_meters(self.level_meters)

    def start_jacktrip_session(self):
        """Start hubserver JackTrip session"""

        self.current_pytrip = noisebox_helpers.PyTrip(self.session_params)
        pytrip_watch = noisebox_helpers.PyTripWatch()
        pytrip_wait = noisebox_helpers.PyTripWait(self.oled, self.active_server)

        try:
            self.current_pytrip.start()
            pytrip_watch.run(self.current_pytrip)
            pytrip_wait.run(pytrip_watch)

        except noisebox_helpers.NoiseBoxCustomError:
            print("Could not start JackTrip session")
            raise

        else:
            self.jackHelper.make_jacktrip_connections(self.active_server)
            self.start_level_meters()

        finally:
            pytrip_watch.terminate()

    def stop_monitoring_audio(self):
        """Stop monitoring audio"""

        self.oled.stop_meters()
        for thread in self.level_meters:
            thread.terminate()
        self.jackHelper.disconnect_session()

    def stop_jacktrip_session(self):
        """Stop JackTrip session"""

        self.stop_monitoring_audio()

        self.current_pytrip.stop()

        self.oled.draw_text(0, 26, "JackTrip stopped")
        sleep(1)


def main():

    menu_items = ['START JACKTRIP',
                  'LEVEL METER',
                  'CONNECTED PEERS',
                  'IP ADDRESS']

    oled = noisebox_oled.OLED()
    jackHelper = noisebox_helpers.JackHelper(oled)

    receive_ports = jackHelper.client.get_ports(is_audio=True, is_output=True)
    for port in receive_ports:
        jackHelper.disconnect_all(port)

    oled_menu = noisebox_oled_helpers.Menu(menu_items)

    noisebox = Noisebox(jackHelper, oled)

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
