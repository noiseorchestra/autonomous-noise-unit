from queue import Empty


class PyTripWait():
    """Watch jacktrip stdout q and wait on connection otherwise timeout"""

    def __init__(self):
        self.waiting = False
        self.message = None
        self.connected = False

    def check_stdout(self, data, peer_ip):

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
            self.message = ['==SUCCESS==',
                            'jacktrip connected!']
            self.connected = True
            self.waiting = False

        if waiting in data:
            self.message = ['==CONNECTING==',
                            waiting]

        for error in errors:
            if error in data:
                self.message = ['==ERROR==', error, 'JackTrip stopped']
                self.waiting = False

        if stopped in data:
            self.message = ['==ERROR==',
                            "Could not connect to: " + peer_ip,
                            stopped]
            self.waiting = False

    def timeout(self):
        self.message = ['==TIMEOUT==',
                        "Waited too long for peer"]
        self.waiting = False

    def run(self, jacktrip_watch, peer_ip):
        """Check q messages and block until connected or timeout"""

        self.waiting = True
        self.connected = False

        while self.waiting is True:
            try:
                data = jacktrip_watch.queue.get(True, timeout=10)
                print(data)
                self.check_stdout(data, peer_ip)
            except Empty:
                self.timeout()
