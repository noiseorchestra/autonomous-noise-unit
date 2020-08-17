import time
from queue import Empty
from noisebox_helpers.custom_exceptions import NoiseBoxCustomError


class PyTripWait():
    """Watch jacktrip stdout q and wait on connection otherwise timeout"""

    def __init__(self, oled, server_ip, jacktrip_monitor):
        self.jacktrip_monitor = jacktrip_monitor
        self.waiting = True
        self.server_ip = server_ip
        self.oled = oled

    def keep_waiting(self, message):
        self.oled.draw_lines(message)

    def stop_waiting_error(self, message):
        print("Error occured stop JackTrip")
        self.waiting = False
        print("Raise NoiseBoxCustomError")
        raise NoiseBoxCustomError(message)

    def stop_waiting_success(self, message):
        self.oled.draw_lines(message)
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
                       'jacktrip connected!']
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
        self.oled.draw_lines(message)
        time.sleep(1)

        while self.waiting is True:
            print("Waiting for jacktrip to start")
            try:
                data = self.jacktrip_monitor.queue.get(True, timeout=10)
                print(data)
                self.check_messages(data)
            except Empty:
                self.timeout()
            except NoiseBoxCustomError:
                raise
