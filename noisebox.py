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
        self.menu = Menu()

    def get_ip(self):
        """Get and return ip and hostname"""

        result = self.nh.ip_address()
        return result

    def get_session_params(self):
        return self.config.get_config()['jacktrip-default']

    def check_peers(self):
        """Check status of all peers"""

        peers = self.config.get_config()['peers']['ip_addresses'].split(',')
        peers.append(self.config.get_config()['jacktrip-default']['peer-ip'])
        self.online_peers = self.nh.get_online_peers(peers)
        return self.online_peers

    def set_level_meters(self, ports, prefix):
        for i, port in enumerate(ports):
            channel = prefix + str(i + 1)
            self.level_meters.append(self.nh.LevelMeter(port.name, channel))

    def is_stereo_input(self):
        return False if self.get_session_params()['input-channels'] is "1" else True

    def start_level_meters(self, jacktrip_session=False):
        """Get relevant ports and start level meters"""

        self.level_meters = []

        try:
            self.set_level_meters(self.jack_helper.get_inputs(self.is_stereo_input()), "IN-")
            if jacktrip_session is True:
                self.set_level_meters(self.jack_helper.get_jacktrip_receives(), "JT-")
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

    def is_session_connected(self, result):
        if result["connected"] is True:
            self.jack_helper.disconnect_session()
            self.oled.draw_lines(result["message"])
            self.start_jacktrip_monitoring()
        else:
            self.pytrip.stop_watching()
            self.pytrip.stop()
            raise self.nh.NoiseBoxCustomError(result["message"])

    def start_jacktrip_session(self):
        """Start hubserver JackTrip session"""

        self.oled.draw_lines(["==START JACKTRIP==", "Connecting to:", self.get_session_params()['ip']])

        result = self.pytrip.connect_to_hub_server(self.get_session_params())
        self.is_session_connected(result)

    def start_jacktrip_peer_session(self, server=True, peer_address=None):

        start_message = ["==START JACKTRIP==", "Starting server", "Waiting for peer.."]
        if server is False:
            start_message = ["==START JACKTRIP==", "Connecting to:", peer_address]

        self.oled.draw_lines(start_message)
        result = self.pytrip.connect_to_peer(self.get_session_params(), server=server, peer_address=peer_address)
        self.is_session_connected(result)

    def stop_jacktrip_session(self):
        """Stop JackTrip session"""

        self.stop_monitoring()
        self.pytrip.stop_watching()
        self.pytrip.stop()
        self.oled.draw_lines(["==JACKTRIP STOPPED=="])

    def restart_jack_if_needed(self):
        new_pps = self.get_session_params()["jack-pps"]
        if self.jack_helper.check_current_pps(new_pps) is False:
            self.oled.draw_lines(["==RESTARTING JACK==", "at " + new_pps + " pps" ])
            self.jack_helper.stop()
            self.jack_helper.start(self.get_session_params())

    def system_update(self):
        p = subprocess.run(["git", "pull"])
        if p.returncode == 1:
            raise self.nh.NoiseBoxCustomError(["==ERROR==", "could not update"])
        self.oled.draw_lines(["==UPDATE==", "Update succesful", "restarting system..."])
        sys.exit("System restart")

    def shutdown(self):
        p = subprocess.run(["sudo", "shutdown", "-h", "now"])

def main():

    import RPi.GPIO as GPIO
    from noisebox_rotary_helpers.rotary import KY040

    noisebox = Noisebox(dry_run=False)
    ky040 = KY040(noisebox)

    try:
        noisebox.oled.draw_logo()
        sleep(3)
        noisebox.menu.start(noisebox.oled.device)
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
        noisebox.jack_helper.start(noisebox.get_session_params())
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
