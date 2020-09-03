from threading import Thread
from subprocess import Popen, PIPE
import math


class LevelMeter:
    """Helper object for live monitoring the volume level of audio channels"""

    def __init__(self, port, name=""):
        self.current_meter_value = 0.0
        self.current_meter = None
        self.port = port
        self._running = True
        self.name = name

        # run meter on init
        self.run()

    def start_meter(self):
        """Start jack_meter process"""

        command = ["jack_meter", self.port, "-n"]
        process = Popen(command, stdout=PIPE)
        self.current_meter = process

    def monitor_jack_meter(self):
        """Open monitor jack_meter and set current_meter_value"""

        while self._running:
            try:
                level = float(str(self.current_meter.stdout.readline().rstrip(), 'utf-8'))
                value = -52.0
                if math.isinf(level) is not True:
                    value = level
                if value < -52.0:
                    value = -52.0
                self.current_meter_value = value

            except ValueError:
                print("level_meter value not float")
                pass

    def run(self):
        """Start meter and run monitor_jack_meter in thread"""

        self.start_meter()

        t = Thread(target=self.monitor_jack_meter)
        t.start()

    def get_current_value(self):
        """Get current_meter_value"""

        return self.current_meter_value

    def terminate(self):
        """Stop current meter thread"""

        self._running = False
        self.current_meter.terminate()
        self.current_meter.wait()
        self.current_meter = None
