from queue import Empty


class PyTripWait():
    """Watch jacktrip stdout q and wait for connection otherwise timeout"""

    def __init__(self):
        self.waiting = False
        self.message = None
        self.connected = False

    def run(self, jacktrip_watch, peer_ip):
        """Run process and block until connection, error or timeout"""

        self.waiting = True
        self.connected = False

        while self.waiting is True:
            try:
                data = jacktrip_watch.queue.get(True, timeout=10)
                print(data)
                self.check_stdout(data, peer_ip)
            except Empty:
                self.timeout()

    def timeout(self):
        """Timeout connection attempt"""

        self.message = ['==TIMEOUT==', "Waited too long for peer"]
        self.connected = False
        self.waiting = False

    def check_stdout(self, data, peer_ip):
        """Check stdout and match to list of messages"""

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
            self.message = ['==SUCCESS==', 'jacktrip connected!']
            self.connected = True
            self.waiting = False

        if waiting in data:
            self.message = ['==CONNECTING==', waiting]

        for error in errors:
            if error in data:
                self.message = ['==ERROR==', error, 'JackTrip stopped']
                self.connected = False
                self.waiting = False

        if stopped in data:
            self.message = ['==ERROR==',
                            "Could not connect to: " + peer_ip,
                            stopped]
            self.connected = False
            self.waiting = False
