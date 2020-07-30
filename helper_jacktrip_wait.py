import oled_helpers
import time
from queue import Queue, Empty


class JacktripWait():
    """Watch jacktrip stdout q and wait on connection otherwise timeout"""

    def __init__(self, server_ip, jacktrip_monitor):
        self.jacktrip_monitor = jacktrip_monitor
        self.waiting = True
        self.server_ip = server_ip
        self.oled_helpers = oled_helpers.OLED_helpers()

    def keep_waiting(self, message):
        self.oled_helpers.draw_lines(message)

    def stop_waiting_error(self, message):
        self.waiting = False
        raise Exception(message)

    def stop_waiting_success(self, message):
        self.oled_helpers.draw_lines(message)
        self.waiting = False
        time.sleep(1)

    def check_messages(self, data):

        success = 'Received Connection from Peer!'
        stopped = 'JackTrip Processes STOPPED!'
        waiting = 'Waiting for Peer...'
        errors = ['Maybe the JACK server is not running',
                  'Unable to connect to JACK server',
                  'JACK server not running',
                  'Peer Buffer Size',
                  'Wrong bit resolution',
                  'Exiting JackTrip']

        if success in data:
            message = ['==SUCCESS==',
                       success,
                       'jacktrip connected to: ' + self.server_ip]
            self.stop_waiting_success(message)

        if waiting in data:
            message = ['==CONNECTING==',
                       waiting]
            self.keep_waiting(message)

        for error in errors:
            if error in data:
                message = ['==ERROR==', error, 'JackTrip stopped']
                self.stop_waiting_error(message)

        if stopped in data:
            message = ['==ERROR==',
                       "Could not connect to: " + self.server_ip,
                       stopped]
            self.stop_waiting_error(message)

    def timeout(self):
        message = ['==TIMEOUT==',
                   "Waited too long for peer"]
        self.stop_waiting_error(message)

    def run(self):
        """Check q messages and block until connected or timeout"""

        message = ['==STARTING==', 'JackTrip starting...']
        self.oled_helpers.draw_lines(message)
        time.sleep(1)

        while self.waiting is True:
            try:
                data = self.jacktrip_monitor.queue.get(True, timeout=10)
                print(data)
                self.check_messages(data)
            except Empty:
                self.timeout()
