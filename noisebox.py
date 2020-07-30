#!/usr/bin/python3

import RPi.GPIO as GPIO
from rotary import KY040
import configparser
from time import sleep
import helper_get_ip
import helper_peers
import oled_helpers
from helper_jacktrip import PyTrip
from helper_channel_meters import ChannelMeters
import jack_helper
import noisebox_menu

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

    def __init__(self, jackHelper):
        self.active_server = default_jacktrip_params['ip']
        self.peers = peers.split(',')
        self.online_peers = peers.split(',')
        self.session_params = default_jacktrip_params
        self.current_jacktrip = None
        self.channel_meters = None
        self.oled_helpers = oled_helpers.OLED_helpers()
        self.jackHelper = jackHelper

    def get_ip(self):
        """Get and return ip"""

        ip = helper_get_ip.ip_address()
        return ip

    def check_peers(self):
        """Check status of all peers and show results"""

        # TO DO
        # Remove self from peers list
        # Make menu to select peer to connect to

        self.oled_helpers.draw_text(0, 26, "Searching for peers...")
        check_peers = helper_peers.Check_Peers()
        peers = check_peers.ping_all(self.peers)
        online_peers = []
        for peer in peers:
            if peer.rc == 0:
                online_peers.append(peer.peer)
        self.online_peers = online_peers
        self.oled_helpers.draw_lines(online_peers)
        # self.start_peer_session()

    def start_monitoring_audio(self):
        """Start monitoring audio"""
        self.jackHelper.make_monitoring_connections()
        port_names = self.jackHelper.get_input_port_names()

        if len(port_names) == 0:
            raise TypeError("No audio inputs found")

        self.channel_meters = ChannelMeters(port_names)

    def start_jacktrip_session(self):
        """Start hubserver JackTrip session"""
        print(self.session_params)
        self.current_jacktrip = PyTrip(self.session_params)

        try:
            self.current_jacktrip.start()
            self.jackHelper.make_jacktrip_connections(self.active_server)
            self.start_monitoring_audio()

        except Exception:
            self.current_jacktrip.stop()
            raise

    # P2P connections function goes here

    def stop_monitoring_audio(self):
        """Stop monitoring audio"""

        self.jackHelper.disconnect_session()
        self.channel_meters.stop()
        self.channel_meters = None

    def stop_jacktrip_session(self):
        """Stop JackTrip session"""

        self.stop_monitoring_audio()

        self.current_jacktrip.stop()
        self.channel_meters = None

        self.oled_helpers.draw_text(0, 26, "JackTrip stopped")
        sleep(1)


def main():

    menu_items = ['SERVER 1',
                  'LEVEL METER',
                  'CONNECTED PEERS',
                  'IP ADDRESS',
                  'TEST LAYOUT']

    jackHelper = jack_helper.JackHelper()

    receive_ports = jackHelper.client.get_ports(is_audio=True, is_output=True)
    for port in receive_ports:
        jackHelper.disconnect_all(port)

    oled_h = oled_helpers.OLED_helpers()
    oled_menu = noisebox_menu.Menu(menu_items)

    noisebox = Noisebox(jackHelper)

    oled_menu.start(noisebox, oled_h)

    ky040 = KY040(noisebox, oled_menu)
    ky040.start()

    try:
        while True:
            sleep(0.1)
    finally:
        ky040.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    main()
