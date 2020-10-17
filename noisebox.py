#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep
import subprocess
import sys
import os
from noisebox_oled_helpers import Menu, OLED
import noisebox_helpers as nh
from noisebox_rotary_helpers.rotary import KY040

class Noisebox:
    """Main noisebox class"""

    def __init__(self, jack_helper, oled, config):
        self.config = config
        self.online_peers = None
        self.pytrip = nh.PyTrip()
        self.oled = OLED()
        self.jack_helper = jack_helper
        self.pytrip_watch = nh.PyTripWatch()
        self.pytrip_wait = nh.PyTripWait()

    def get_ip(self):
        """Get and return ip and hostname"""

        result = nh.ip_address()
        return result

    def get_session_params(self):
        return self.config.get_config()['jacktrip-default']

    def check_peers(self):
        """Check status of all peers"""

        peers = self.config.get_config()['peers']['ip_addresses'].split(',')
        self.online_peers = nh.get_online_peers(peers)
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

        stereo_input = False if self.get_session_params()['input-channels'] is "1" else True
        self.start_level_meters(stereo_input=stereo_input)
        self.jack_helper.make_monitoring_connections(stereo_input=stereo_input)

    def start_jacktrip_monitoring(self):
        """Start monitoring jacktrip session audio"""

        stereo_jacktrip = False if self.get_session_params()['jacktrip-channels'] == "1" else True
        stereo_input = False if self.get_session_params()['input-channels'] == "1" else True
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
            self.oled.draw_lines(["==START JACKTRIP==", "Connecting to:", self.get_session_params()['ip']])
            self.pytrip.start(self.get_session_params())
        except Exception:
            self.pytrip.stop()
            raise nh.NoiseBoxCustomError(["==JACKTRIP ERROR==", "JackTrip failed to start"])
        else:
            self.pytrip_watch.run(self.pytrip)
            self.pytrip_wait.run(self.pytrip_watch, self.get_session_params()['ip'])
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
            self.pytrip.start(self.get_session_params(), p2p=True, server=server, peer_address=peer_address)
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

    def system_update(self):
        p = subprocess.run(["git", "pull"])
        if p.returncode == 1:
            raise nh.NoiseBoxCustomError(["==ERROR==", "could not update"])
        self.oled.draw_lines(["==UPDATE==", "Update succesful", "restarting system..."])
        sys.exit("System restart")


def main():

    config = nh.Config()

    menu_items = nh.menu.get_main_menu_items()
    settings_items = nh.menu.get_settings_items(config)
    advanced_settings_items = nh.menu.get_advanced_settings_items(config)

    jack_helper = nh.JackHelper()
    menu = Menu(menu_items, settings_items, advanced_settings_items)
    noisebox = Noisebox(jack_helper, config)
    ky040 = KY040(noisebox, menu)

    try:
        menu.start(noisebox.oled.device)
    except Exception as e:
        print("OLED error:", e)
        sys.exit("Exited because of OLED error")

    try:
        ky040.start()
    except Exception as e:
        print("Rotary switch error: ", e)
        noisebox.oled.draw_lines(["==ERROR==", "Rotary switch error", "Restarting noisebox"])
        sleep(4)
        sys.exit("Exited because of rotary error")

    try:
        jack_helper.start()
    except Exception as e:
        print("JACK Client could not start:", e)
        noisebox.oled.draw_lines(["==ERROR==", "JACK didn't start", "Restarting script"])
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
