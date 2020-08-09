from threading import Thread
from helper_channel_meter import ChannelMeter
from oled_meters import Meters
from oled_helpers import OLED_helpers


class ChannelMeters:
    def __init__(self, port_names):
        self.oled_helpers = OLED_helpers()
        self.current_meters = self.start(port_names)
        self.jack_meter_threads = None

    def get_jack_meter_threads(self, channels):
        """Monitor array of channels and return threads"""

        jack_meter_threads = []
        for channel in channels:
            command = ["jack_meter", channel, "-n"]
            jack_meter_thread = ChannelMeter(command)
            jack_meter_thread.run()
            jack_meter_threads.append(jack_meter_thread)
        return jack_meter_threads

    def start(self, port_names):
        """Start drawing OLED meters"""

        current_meters = Meters()
        jack_meter_threads = self.get_jack_meter_threads(port_names)
        self.jack_meter_threads = jack_meter_threads

        t = Thread(
            target=current_meters.render,
            args=(self.oled_helpers.device, jack_meter_threads,))

        t.start()

        self.current_meters = current_meters

        return current_meters

    def stop(self):
        """Stop drawing OLED meters"""
        print("STOP METERS")
        self.current_meters.terminate()
