#!/usr/bin/python3

import RPi.GPIO as GPIO
import configparser as cp
from time import sleep
import sys
import os
import noisebox_rotary_helpers
import noisebox_oled_helpers
import noisebox_helpers as nh

cfg = cp.ConfigParser(interpolation=cp.ExtendedInterpolation())
cfg.read('config.ini')


class Noisebox:
    """Main noisebox class"""

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
        """Get and return ip and hostname"""

        result = nh.ip_address()
        return result

    def check_peers(self):
        """Check status of all peers"""

        self.online_peers = nh.get_online_peers(self.peers)
        return self.online_peers

    def start_level_meters(self, stereo=False, jacktrip_session=False):
        """Get relevant ports and start level meters"""

        level_meters = []

        try:
            local_inputs = self.jack_helper.get_inputs(stereo=stereo)
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

        stereo = False if self.session_params['channels'] is "1" else True
        self.start_level_meters(stereo=stereo)
        self.jack_helper.make_monitoring_connections(stereo=stereo)

    def start_jacktrip_monitoring(self):
        """Start monitoring jacktrip session audio"""

        stereo = False if self.session_params['channels'] is "1" else True
        self.start_level_meters(stereo=stereo, jacktrip_session=True)
        self.jack_helper.make_jacktrip_connections(self.current_server, stereo=stereo)

    def stop_monitoring(self):
        """Stop monitoring audio"""

        self.oled.stop_meters()
        for thread in self.level_meters:
            thread.terminate()
        self.jack_helper.disconnect_session()

    def start_jacktrip_session(self):
        """Start hubserver JackTrip session"""

        try:
            self.oled.draw_lines(["==START JACKTRIP==", "Connecting to:", self.current_server])
            self.pytrip.start(self.session_params)
        except Exception:
            self.pytrip.stop()
            raise nh.NoiseBoxCustomError(["==JACKTRIP ERROR==", "JackTrip failed to start"])
        else:
            self.pytrip_watch.run(self.pytrip)
            self.pytrip_wait.run(self.pytrip_watch, self.current_server)
            message = self.pytrip_wait.message

            if self.pytrip_wait.connected is True:
                self.jack_helper.disconnect_session()
                self.oled.draw_lines(message)
                self.start_jacktrip_monitoring()
            else:
                self.pytrip_watch.terminate()
                self.pytrip.stop()
                raise nh.NoiseBoxCustomError(message)

    def start_jacktrip_peer_session_client(self, peer_address):

        self.oled.draw_lines(["==START JACKTRIP==", "Connecting to:", peer_address])
        try:
            self.pytrip.start(self.session_params,
                              server=False,
                              p2p=True,
                              peer_address=peer_address)
        except Exception:
            self.pytrip.stop()
            raise nh.NoiseBoxCustomError(["==JACKTRIP ERROR==", "JackTrip failed to start"])
        else:
            self.pytrip_watch.run(self.pytrip)
            self.pytrip_wait.run(self.pytrip_watch, peer_address)
            message = self.pytrip_wait.message

            if self.pytrip_wait.connected is True:
                self.jack_helper.disconnect_session()
                self.oled.draw_lines(message)
                self.start_jacktrip_monitoring()
            else:
                self.pytrip.stop()
                self.pytrip_watch.terminate()

    def start_jacktrip_peer_session_server(self):
        self.oled.draw_lines(["==START JACKTRIP==", "Starting server", "Waiting for peer.."])
        try:
            self.pytrip.start(self.session_params,
                              server=True,
                              p2p=True)
        except Exception:
            self.pytrip.stop()
            raise nh.NoiseBoxCustomError(["==JACKTRIP ERROR==", "JackTrip failed to start"])
        else:
            self.pytrip_watch.run(self.pytrip)
            self.pytrip_wait.run(self.pytrip_watch, "server")
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


def main():

    menu_items = ['START JACKTRIP',
                  'LEVEL METER',
                  'P2P SESSION',
                  'IP ADDRESS',
                  'SETTINGS']

    oled = noisebox_oled_helpers.OLED()
    jack_helper = nh.JackHelper()
    oled_menu = noisebox_oled_helpers.Menu(menu_items)
    noisebox = Noisebox(jack_helper, oled)
    ky040 = noisebox_rotary_helpers.KY040(noisebox, oled_menu)
    oled_menu.start(noisebox.oled.device)

    try:
        ky040.start()
    except Exception as e:
        print("Rotary switch error: ", e)
        oled.draw_lines(["==ERROR==", "Rotary switch error", "Restarting noisebox"])
        sleep(4)
        sys.exit("Exited because of rotary error")

    try:
        oled_menu.start(noisebox.oled.device)
    except Exception as e:
        print("OLED error:", e)
        sys.exit("Exited because of OLED error")

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
