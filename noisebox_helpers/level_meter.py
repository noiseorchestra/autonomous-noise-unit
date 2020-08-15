from threading import Thread
from subprocess import Popen, PIPE
import math


class LevelMeter:
    """Helper object for live monitoring the volume level of audio channels"""

    def __init__(self, command):
        self.current_meter_value = 0.0
        self.command = command
        self._running = True

    def set_meter_value(self, process):
        level = float(str(process.stdout.readline().rstrip(), 'utf-8'))
        self.current_meter_value = -62 if math.isinf(level) else level

    def level_meter(self, command):
        """Open process and push stdout to queue"""

        process = Popen(command, stdout=PIPE)
        while self._running:
            self.set_meter_value(process)

    def get_current_value(self):
        """Get current value"""
        return self.current_meter_value

    def run(self):
        """Run producer and consumer threads"""

        t = Thread(target=self.level_meter, args=(self.command,))
        t.start()

    def terminate(self):
        self._running = False
