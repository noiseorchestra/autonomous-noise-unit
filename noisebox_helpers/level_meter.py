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

        self.run()

    def set_meter_value(self):
        try:
            level = float(str(self.current_meter.stdout.readline().rstrip(), 'utf-8'))
            self.current_meter_value = -62 if math.isinf(level) else level

        except ValueError:
            print("level_meter value not float")
            pass

    def get_current_value(self):
        """Get current value"""
        return self.current_meter_value

    def level_meter(self, port):
        """Open process and push stdout to queue"""

        command = ["jack_meter", port, "-n"]
        process = Popen(command, stdout=PIPE)
        self.current_meter = process

        while self._running:
            self.set_meter_value()

    def run(self):
        """Run in thread"""

        t = Thread(target=self.level_meter, args=(self.port,))
        t.start()

    def terminate(self):
        self._running = False
        self.current_meter.terminate()
        self.current_meter.wait()
        self.current_meter = None
        print("level_meter process terminated")
