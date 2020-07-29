from threading import Thread
from helper_channel_meter import ChannelMeter
from oled_meters import Meters
from oled_helpers import OLED_helpers


class ChannelMeters:
    def __init__(self, port_names):
        self.oled_helpers = OLED_helpers()
        self.current_meters = self.start(port_names)

        if self.channel_meters is None:
            return None

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

        if len(port_names) != 0:
            current_meters = Meters()
            meter_threads = self.get_meter_threads(port_names)

            t = Thread(
                target=current_meters.render,
                args=(self.oled_helpers.get_device(), meter_threads,))
            t.start()
            return current_meters
        else:
            self.oled_helpers.draw_text(0, 26, "No input ports detected")
            return None

    def stop(self):
        """Stop drawing OLED meters"""

        self.current_meters.terminate()
        self.channel_meters = None
