#!/usr/bin/python3
from time import sleep
import subprocess
import sys
from noisebox_oled_helpers import Menu, OLED
import noisebox_helpers as nh


class Noisebox:
    """Main noisebox class"""

    def __init__(self, dry_run):
        self.config = None
        self.online_peers = []
        self.pytrip = None
        self.oled = None
        self.jack_helper = None
        self.pytrip_watch = None
        self.pytrip_wait = None
        self.level_meters = []

        self.set_attributes(dry_run)

    def set_attributes(self, dry_run):
        if dry_run is True:
            self.config = nh.Config(dry_run)
            return

        self.nh = nh
        self.config = nh.Config()
        self.pytrip = nh.PyTrip()
        self.oled = OLED()
        self.jack_helper = nh.JackHelper()
        self.pytrip_watch = nh.PyTripWatch()
        self.pytrip_wait = nh.PyTripWait()

    def get_ip(self):
        """Get and return ip and hostname"""

        result = self.nh.ip_address()
        return result

    def get_session_params(self):
        return self.config.get_config()['jacktrip-default']

    def check_peers(self):
        """Check status of all peers"""

        peers = self.config.get_config()['peers']['ip_addresses'].split(',')
        self.online_peers = self.nh.get_online_peers(peers)
        return self.online_peers

    def set_level_meters(self, ports):
        for i, port in enumerate(ports):
            channel = "IN-" + str(i + 1)
            self.level_meters.append(self.nh.LevelMeter(port.name, channel))

    def is_stereo_input(self):
        return False if self.get_session_params()['input-channels'] is "1" else True

    def start_level_meters(self, jacktrip_session=False):
        """Get relevant ports and start level meters"""

        self.level_meters = []

        try:
            self.set_level_meters(self.jack_helper.get_inputs(self.is_stereo_input()))
            if jacktrip_session is True:
                self.set_level_meters(self.jack_helper.get_jacktrip_receives())
        except self.nh.NoiseBoxCustomError:
            raise
        else:
            self.oled.start_meters(self.level_meters)

    def start_local_monitoring(self):
        """Start monitoring local audio"""

        self.start_level_meters()
        self.jack_helper.make_monitoring_connections(self.is_stereo_input())

    def start_jacktrip_monitoring(self):
        """Start monitoring jacktrip session audio"""

        self.start_level_meters(jacktrip_session=True)
        self.jack_helper.make_jacktrip_connections(self.is_stereo_input())

    def stop_monitoring(self):
        """Stop monitoring audio"""

        self.oled.stop_meters()
        for thread in self.level_meters:
            thread.terminate()
        self.jack_helper.disconnect_session()

    def start_jacktrip_session(self):
        """Start hubserver JackTrip session"""

        self.oled.draw_lines(["==START JACKTRIP==", "Connecting to:", self.get_session_params()['ip']])

        result = self.pytrip.connect_to_hub_server(self.get_session_params())

        if result.connected is True:
            self.jack_helper.disconnect_session()
            self.oled.draw_lines(result.message)
            self.start_jacktrip_monitoring()
        else:
            self.pytrip.stop_watching()
            self.pytrip.stop()
            raise self.nh.NoiseBoxCustomError(result.message)

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
            raise self.nh.NoiseBoxCustomError(error_message)
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
                raise self.nh.NoiseBoxCustomError(message)

    def stop_jacktrip_session(self):
        """Stop JackTrip session"""

        self.stop_monitoring()
        self.pytrip_watch.terminate()
        self.pytrip.stop()
        self.oled.draw_lines(["==JACKTRIP STOPPED=="])

    def system_update(self):
        p = subprocess.run(["git", "pull"])
        if p.returncode == 1:
            raise self.nh.NoiseBoxCustomError(["==ERROR==", "could not update"])
        self.oled.draw_lines(["==UPDATE==", "Update succesful", "restarting system..."])
        sys.exit("System restart")


def main():

    import RPi.GPIO as GPIO
    from noisebox_rotary_helpers.rotary import KY040

    noisebox = Noisebox(dry_run=False)

    menu_items = nh.menu.get_main_menu_items()
    settings_items = nh.menu.get_settings_items(noisebox.config)
    advanced_settings_items = nh.menu.get_advanced_settings_items(noisebox.config)

    menu = Menu(menu_items, settings_items, advanced_settings_items)
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
        noisebox.jack_helper.start()
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
