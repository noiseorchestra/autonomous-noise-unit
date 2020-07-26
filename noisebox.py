import RPi.GPIO as GPIO
from rotary import KY040
from configparser import ConfigParser
from threading import Thread
from time import sleep
import helper_get_ip
import helper_threaded_meter
import helper_peers
import oled_helpers
import oled_meters
import helper_jacktrip
import jack_helper
import noisebox_menu

cfg = ConfigParser()
cfg.read('config.ini')
peers = cfg.get('peers', 'ips')


class Noisebox:
    """Main noisebox object"""

    def __init__(self, jackHelper):
        self.server1_ip = cfg.get('server1', 'ip')
        self.server2_ip = cfg.get('server2', 'ip')
        self.active_server = cfg.get('server1', 'ip')
        self.peers = peers.split(',')
        self.online_peers = peers.split(',')
        self.server1_params = {'hub_mode': True, 'server': False,
                               'ip': self.server1_ip, 'channels': "1",
                               'queue': "4"}
        self.default_peer_params = {'hub_mode': False, 'ip': "",
                                    'server': True, 'channels': "1",
                                    'queue': "4"}
        self.current_peer_params = {}
        self.session_active = False
        self.current_session = None
        self.current_meters = None
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

    def start_peer_session(self):
        """Start peer 2 peer JackTrip session"""

        # TODO
        # use OLED menu to connect to chosen peer

        if len(self.online_peers) == 1:
            self.current_session_params = self.default_peer_params
            self.oled_helpers.draw_text(0, 26, "Starting JackTrip as server")
        else:
            self.current_session_params = self.default_peer_params
            self.current_session_params.update({'ip': self.online_peers[0],
                                                'server': False})
            self.oled_helpers.draw_text(0, 26, "Starting JackTrip as client")

        self.current_session = helper_jacktrip.PyTrip(self.current_session_params)
        self.current_session.start()

        # not tested this section

        if self.current_session.jacktrip_monitor.jacktrip_connected is True:
            self.session_active = True

        self.start_meters()

    def start_session(self):
        """Start hubserver JackTrip session"""
        # TO DO
        # Eventually pass in different server params..
        # depending on which server we are connecting to
        # Refactor code, make more DRY
        self.active_server = self.server1_ip
        self.current_session_params = self.server1_params
        self.current_session = helper_jacktrip.PyTrip(self.current_session_params)
        self.oled_helpers.draw_text(0, 26, "Connecting to server...")
        self.current_session.start()

        if self.current_session.jacktrip_monitor.jacktrip_connected is True:
            self.session_active = True

            # Refactor this into own function
            receive_ports = self.jackHelper.client.get_ports(is_audio=True, is_output=True, is_physical=True)
            local_send_ports = self.jackHelper.client.get_ports('system:playback.*')
            jacktrip_send_ports = self.jackHelper.client.get_ports(self.active_server + ':send.*')
            jacktrip_receive_ports = self.jackHelper.client.get_ports(self.active_server + ':receive.*')
            self.jackHelper.connect_ports(receive_ports, [jacktrip_send_ports])
            self.jackHelper.connect_ports(jacktrip_receive_ports, [local_send_ports])

            self.start_meters()

    def stop_session(self):
        """Stop JackTrip session"""

        self.current_meters.terminate()
        self.current_session.stop()

        self.session_active = False
        self.current_session = None
        self.current_meters = None

        self.oled_helpers.draw_text(0, 26, "JackTrip stopped")

        sleep(1)

    def monitor_channels(self, channels):
        """Monitor array of channels and return threads"""

        threads = []
        for channel in channels:
            command = "jack_meter " + channel + " -n"
            meter_thread = helper_threaded_meter.ThreadedMeter(command)
            meter_thread.run()
            threads.append(meter_thread)
        return threads

    def start_meters(self):
        """Start drawing OLED meters"""

        port_names = self.jackHelper.get_input_port_names()
        meter_threads = self.monitor_channels(port_names)
        self.current_meters = oled_meters.Meters()
        t = Thread(
            target=self.current_meters.render,
            args=(self.oled_helpers.get_device(), meter_threads,))
        t.start()

    def stop_meters(self):
        """Stop drawing OLED meters"""
        receive_ports = self.jackHelper.client.get_ports('lounge-music.*')
        for port in receive_ports:
            self.jackHelper.disconnect_all(port)

        self.current_meters.terminate()
        self.current_meters = None


def main():

    CLOCKPIN = 18
    DATAPIN = 17
    SWITCHPIN = 27

    jackHelper = jack_helper.JackHelper(['jackd', '-dalsa', '-r48000'])
    receive_ports = jackHelper.client.get_ports(is_audio=True, is_output=True)
    for port in receive_ports:
        jackHelper.disconnect_all(port)
    noisebox = Noisebox(jackHelper)
    oled_h = oled_helpers.OLED_helpers()
    oled_menu = noisebox_menu.Menu(['ROOM 1',
                                    'LEVEL METER',
                                    'TEST',
                                    'P2P',
                                    'IPAddress'], oled_h, noisebox)

    def rotaryChange(direction):
        if noisebox.current_meters is None:
            oled_menu.counter
            if direction == 1:
                oled_menu.counter += 1
            else:
                oled_menu.counter -= 1
            oled_menu.draw_menu()

    def switchPressed():
        if noisebox.session_active:
            noisebox.stop_session()
            oled_menu.draw_menu()
        elif noisebox.current_meters:
            noisebox.stop_meters()
            oled_menu.draw_menu()
        else:
            strval = oled_menu.names[oled_menu.menuindex]
            oled_menu.menu_operation(strval)

    GPIO.setmode(GPIO.BCM)

    ky040 = KY040(CLOCKPIN, DATAPIN, SWITCHPIN,
                  rotaryChange, switchPressed)
    ky040.start()
    oled_menu.draw_menu()

    try:
        while True:
            sleep(0.1)
    finally:
        ky040.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    main()
