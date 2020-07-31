from threading import Thread
from subprocess import Popen, PIPE
import psutil


class ChannelMeter:
    """Helper object for live monitoring the volume level of audio channels"""

    def __init__(self, command):
        self.current_meter_value = 0
        self.command = command
        self._running = True

    def terminate(self):
        self._running = False

    def level_monitor(self, command):
        """Open process and push stdout to queue"""

        process = Popen(command, stdout=PIPE, shell=True)
        level = 0
        while self._running:
            # Produce some data
            line = process.stdout.readline().rstrip()
            try:
                level = int(float(str(line, 'utf-8')))
                print("from meter:", level)
            except (OverflowError, ValueError):
                pass
            finally:
                self.current_meter_value = level

        process.terminate()
        process.wait()

    def get_current_value(self):
        """Get current value"""
        return self.current_meter_value

    def run(self):
        """Run producer and consumer threads"""

        t = Thread(target=self.level_monitor, args=(self.command,))
        t.start()
