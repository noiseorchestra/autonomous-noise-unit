from threading import Thread
from helper_channel_meter import ChannelMeter
from oled_meters import Meters
from oled_helpers import OLED_helpers


class ChannelMeters:
    def __init__(self, port_names):
        self.oled_helpers = OLED_helpers()
        self.current_meters = self.start(port_names)

    def get_meter_threads(self, channels):
        """Monitor array of channels and return threads"""

        threads = []
        for channel in channels:
            command = "jack_meter " + channel + " -n"
            meter_thread = ChannelMeter(command)
            meter_thread.run()
            threads.append(meter_thread)
        return threads

    def start(self, port_names):
        """Start drawing OLED meters"""

        current_meters = Meters()
        meter_threads = self.get_meter_threads(port_names)

        t = Thread(
            target=current_meters.render,
            args=(self.oled_helpers.device, meter_threads,))
        t.start()

        self.current_meters = current_meters

        return current_meters

    def stop(self):
        """Stop drawing OLED meters"""

        self.current_meters.terminate()
        self.channel_meters = None
