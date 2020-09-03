#!/usr/bin/python3

import RPi.GPIO as GPIO
import configparser as cp
from time import sleep
import sys
import os
import noisebox_rotary_helpers
import noisebox_oled_helpers
import noisebox_helpers as nh


class Noisebox:
    """Main noisebox class"""

    def __init__(self, cfg, jack_helper, oled):
        self.config = cfg
        self.peers = cfg.get('peers', 'ip_addresses').split(',')
        self.online_peers = None
        self.session_params = cfg['jacktrip-default']
        self.pytrip = nh.PyTrip()
        self.oled = oled
        self.jack_helper = jack_helper
        self.pytrip_watch = nh.PyTripWatch()
        self.pytrip_wait = nh.PyTripWait()

    def get_ip(self):
        """Get and return ip and hostname"""

        result = nh.ip_address()
        return result

    def check_peers(self):
        """Check status of all peers"""

        self.online_peers = nh.get_online_peers(self.peers)
        return self.online_peers

    def start_level_meters(self, stereo_input=False, jacktrip_session=False):
        """Get relevant ports and start level meters"""

        level_meters = []

        try:
            local_inputs = self.jack_helper.get_inputs(stereo=stereo_input)
            for i, port in enumerate(local_inputs):
                channel = "IN-" + str(i + 1)
                level_meters.append(nh.LevelMeter(port.name, channel))

            if jacktrip_session is True:
                jacktrip_receives = self.jack_helper.get_jacktrip_receives()
                for i, port in enumerate(jacktrip_receives):
                    channel = "JT-" + str(i + 1)
                    level_meters.append(nh.LevelMeter(port.name, channel))
        except nh.NoiseBoxCustomError:
            raise
        else:
            self.level_meters = level_meters
            self.oled.start_meters(self.level_meters)

    def start_local_monitoring(self):
        """Start monitoring local audio"""

        stereo_input = False if self.session_params['input-channels'] is "1" else True
        self.start_level_meters(stereo_input=stereo_input)
        self.jack_helper.make_monitoring_connections(stereo_input=stereo_input)

    def start_jacktrip_monitoring(self):
        """Start monitoring jacktrip session audio"""

        stereo_jacktrip = False if self.session_params['jacktrip-channels'] == "1" else True
        stereo_input = False if self.session_params['input-channels'] == "1" else True
        self.start_level_meters(stereo_input=stereo_input, jacktrip_session=True)
        self.jack_helper.make_jacktrip_connections(stereo_input=stereo_input)

    def stop_monitoring(self):
        """Stop monitoring audio"""

        self.oled.stop_meters()
        for thread in self.level_meters:
            thread.terminate()
        self.jack_helper.disconnect_session()

    def start_jacktrip_session(self):
        """Start hubserver JackTrip session"""

        try:
            self.oled.draw_lines(["==START JACKTRIP==", "Connecting to:", self.session_params['ip']])
            self.pytrip.start(self.session_params)
        except Exception:
            self.pytrip.stop()
            raise nh.NoiseBoxCustomError(["==JACKTRIP ERROR==", "JackTrip failed to start"])
        else:
            self.pytrip_watch.run(self.pytrip)
            self.pytrip_wait.run(self.pytrip_watch, self.session_params['ip'])
            message = self.pytrip_wait.message

            if self.pytrip_wait.connected is True:
                self.jack_helper.disconnect_session()
                self.oled.draw_lines(message)
                self.start_jacktrip_monitoring()
            else:
                self.pytrip_watch.terminate()
                self.pytrip.stop()
                raise nh.NoiseBoxCustomError(message)

    def start_jacktrip_peer_session(self, server=True, peer_address=None):

        start_message = ["==START JACKTRIP==", "Starting server", "Waiting for peer.."]
        error_message = ["==JACKTRIP ERROR==", "JackTrip failed to start"]
        peer_address_or_server = "server"
        long_timeout = True

        if server is False:
            start_message = ["==START JACKTRIP==", "Connecting to:", peer_address]
            peer_address_or_server = peer_address
            long_timeout = False

        self.oled.draw_lines(start_message)

        try:
            self.pytrip.start(self.session_params, p2p=True, server=server, peer_address=peer_address)
        except Exception:
            self.pytrip.stop()
            raise nh.NoiseBoxCustomError(error_message)
        else:
            self.pytrip_watch.run(self.pytrip)
            self.pytrip_wait.run(self.pytrip_watch, peer_address_or_server, long_timeout=long_timeout)
            message = self.pytrip_wait.message

            if self.pytrip_wait.connected is True:
                self.jack_helper.disconnect_session()
                self.oled.draw_lines(message)
                self.start_jacktrip_monitoring()
            else:
                self.pytrip.stop()
                self.pytrip_watch.terminate()
                raise nh.NoiseBoxCustomError(message)

    def stop_jacktrip_session(self):
        """Stop JackTrip session"""

        self.stop_monitoring()
        self.pytrip_watch.terminate()
        self.pytrip.stop()
        self.oled.draw_lines(["==JACKTRIP STOPPED=="])

    def save_settings(self):
        self.config['jacktrip-default']['ip'] = self.session_params['ip']
        self.config['jacktrip-default']['jacktrip-channels'] = self.session_params['jacktrip-channels']
        self.config['jacktrip-default']['input-channels'] = self.session_params['input-channels']
        with open('./config.ini', 'w') as configfile:
            self.config.write(configfile)

def main():

    cfg = cp.ConfigParser(interpolation=cp.ExtendedInterpolation())
    if os.path.isfile('./config.ini'):
        cfg.read('./config.ini')
    else:
        print("""
        config.ini file not found, reading example-config.ini instead,
        please create your own config.ini file.
        """)
        cfg.read('./example-config.ini')

    menu_items = ['CONNECT TO SERVER',
                  'LEVEL METER',
                  'P2P SESSION',
                  'SETTINGS -->']

    selected_menu_items = []
    if cfg['jacktrip-default']['input-channels'] == '1':
        selected_menu_items.append('MONO INPUT')

    if cfg['jacktrip-default']['jacktrip-channels'] == '1':
        selected_menu_items.append('MONO JACKTRIP')

    if cfg['jacktrip-default']['ip'] == cfg['server1']['ip']:
        selected_menu_items.append('SERVER A')

    if cfg['jacktrip-default']['ip'] == cfg['server2']['ip']:
        selected_menu_items.append('SERVER B')

    oled = noisebox_oled_helpers.OLED()
    jack_helper = nh.JackHelper()
    oled_menu = noisebox_oled_helpers.Menu(menu_items, selected_menu_items)
    noisebox = Noisebox(cfg, jack_helper, oled)
    ky040 = noisebox_rotary_helpers.KY040(noisebox, oled_menu)
    oled_menu.start(noisebox.oled.device)

    try:
        oled_menu.start(noisebox.oled.device)
    except Exception as e:
        print("OLED error:", e)
        sys.exit("Exited because of OLED error")

    try:
        ky040.start()
    except Exception as e:
        print("Rotary switch error: ", e)
        oled.draw_lines(["==ERROR==", "Rotary switch error", "Restarting noisebox"])
        sleep(4)
        sys.exit("Exited because of rotary error")

    try:
        jack_helper.start()
    except Exception as e:
        print("JACK Client could not start:", e)
        oled.draw_lines(["==ERROR==", "JACK didn't start", "Restarting script"])
        sleep(4)
        sys.exit("Exited because jackd not running")

    try:
        while True:
            sleep(0.1)
    finally:
        ky040.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    main()
