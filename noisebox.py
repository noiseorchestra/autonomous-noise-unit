from configparser import ConfigParser
from threading import Thread
from time import sleep
import helper_get_ip
import helper_threaded_meter
import helper_peers
import oled_helpers
import oled_meters
import pytrip


cfg = ConfigParser()
cfg.read('config.ini')
peers = cfg.get('peers', 'ips')


class Noisebox:
    """Main noisebox object"""

    def __init__(self):
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
        # when OLED menu is ready connect to chosen peer

        if len(self.online_peers) == 1:
            self.current_session_params = self.default_peer_params
            self.oled_helpers.draw_text(0, 26, "Starting JackTrip as server")
        else:
            self.current_session_params = self.default_peer_params
            self.current_session_params.update({'ip': self.online_peers[0],
                                                'server': False})
            self.oled_helpers.draw_text(0, 26, "Starting JackTrip as client")

        self.current_session = pytrip.PyTrip(self.current_session_params)
        self.current_session.start()
        # self.session_active = self.current_session.monitor()
        # if self.session_active:
        #     self.oled_helpers.draw_text(0, 26, "Jacktrip Connected")
        #     # TO DO
        #     # start monitoring JackTrip and handle errors or disconnects
        #     # Eventually meter session from here
        # else:
        #     self.oled_helpers.draw_text(0, 26, "Jacktrip could not connect")
        #     sleep(1)

    def start_session(self):
        """Start hubserver JackTrip session"""
        # TO DO
        # Eventually pass in different server params..
        # depending on which server we are connecting to
        # Refactor code, make more DRY

        self.current_session_params = self.server1_params
        self.current_session = pytrip.PyTrip(self.current_session_params)
        self.oled_helpers.draw_text(0, 26, "Connecting to server...")
        self.current_session.start()

        if self.current_session.jacktrip_monitor.jacktrip_connected is True:
            self.session_active = True
            command = [
                "lounge-music:1",
                "lounge-music:2",
                self.active_server + ":receive_1",
                self.active_server + ":receive_2"
            ]

            self.start_meters(command)

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

    def start_meters(self, channels):
        """Start drawing OLED meters"""

        meter_threads = self.monitor_channels(channels)
        self.current_meters = oled_meters.Meters()
        t = Thread(
            target=self.current_meters.render,
            args=(self.oled_helpers.get_device(), meter_threads,))
        t.start()

    def stop_meters(self):
        """Stop drawing OLED meters"""

        self.current_meters.terminate()
        self.current_meters = None
