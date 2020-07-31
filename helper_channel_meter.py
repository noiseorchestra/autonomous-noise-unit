from threading import Thread
from subprocess import Popen, PIPE
import math


class ChannelMeter:
    """Helper object for live monitoring the volume level of audio channels"""

    def __init__(self, command):
        self.current_meter_value = 0.0
        self.command = command
        self._running = True

    def terminate(self):
        self._running = False

    def level_monitor(self, command):
        """Open process and push stdout to queue"""

        process = Popen(command, stdout=PIPE)
        while self._running:
            # Produce some data
            level = float(str(process.stdout.readline().rstrip(), 'utf-8'))
            self.current_meter_value = -62 if math.isinf(level) else level

        print("JACK_METER THREAD BEING TERMINATED")
        process.terminate()
        process.wait()
        print("JACK_METER THREAD TERMINATED")

    def get_current_value(self):
        """Get current value"""
        return self.current_meter_value

    def run(self):
        """Run producer and consumer threads"""

        t = Thread(target=self.level_monitor, args=(self.command,))
        t.start()
