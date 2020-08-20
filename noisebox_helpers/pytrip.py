from subprocess import Popen, PIPE, STDOUT

class PyTrip:
    """Helper object to start, monitor and disconnect JackTrip"""

    def __init__(self):
        self.current_jacktrip = None
        self.connected = False

    def generate_command(self, params):
        """Generate JackTrip command"""

        ip = params["ip"]
        n = "-n" + params["channels"]
        q = "-q" + params["queue"]

        return ["jacktrip", "-C", ip, n, q, "-z"]

    def start(self, params):
        """Start JackTrip with relevent parameters"""

        command = self.generate_command(params)

        self.current_jacktrip = Popen(command, stdout=PIPE, stderr=STDOUT)

    def stop(self):
        """Stop JackTrip"""
        self.current_jacktrip.terminate()
        self.current_jacktrip.wait()
