from threading import Thread
from subprocess import Popen, PIPE
import math


class LevelMeter:
    """Helper object for live monitoring the volume level of audio channels"""

    def __init__(self, command):
        self.current_meter_value = 0.0
        self.current_meter = None
        self.command = command
        self._running = True

    def set_meter_value(self):
        try:
            level = float(str(self.current_meter.stdout.readline().rstrip(), 'utf-8'))
            self.current_meter_value = -62 if math.isinf(level) else level

        except ValueError:
            print("level_meter value not float")
            pass

    def level_meter(self, command):
        """Open process and push stdout to queue"""

        process = Popen(command, stdout=PIPE)
        self.current_meter = process

        while self._running:
            self.set_meter_value()

    def get_current_value(self):
        """Get current value"""
        return self.current_meter_value

    def run(self):
        """Run producer and consumer threads"""

        t = Thread(target=self.level_meter, args=(self.command,))
        t.start()

    def terminate(self):
        self._running = False
        self.current_meter.terminate()
        self.current_meter.wait()
        self.current_meter = None
        print("level_meter process terminated")
