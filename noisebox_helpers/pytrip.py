from subprocess import Popen, PIPE, STDOUT

class PyTrip:
    """Helper object to start, monitor and disconnect JackTrip"""

    def __init__(self):
        self.current_jacktrip = None
        self.connected = False

    def start(self, params):
        """Start JackTrip with relevent parameters"""

        ip = params["ip"]
        n = "-n" + params["channels"]
        q = "-q" + params["queue"]

        self.current_jacktrip = Popen(["jacktrip", "-C", ip, n, q, "-z"],
                                      stdout=PIPE,
                                      stderr=STDOUT)

    def stop(self):
        """Stop JackTrip"""
        self.current_jacktrip.terminate()
        self.current_jacktrip.wait()
