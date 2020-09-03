from subprocess import Popen, PIPE, STDOUT

class PyTrip:
    """Helper object to start, monitor and disconnect JackTrip"""

    def __init__(self):
        self.current_jacktrip = None
        self.connected = False

    def generate_client_command(self, params, p2p=False, peer_address=None):
        """Generate JackTrip command"""

        ip = params["ip"] if p2p is not True else peer_address
        n = "-n" + params["channels"]
        q = "-q" + params["queue"]
        server_type = "-C" if p2p is not True else "-c"

        return ["jacktrip", server_type, ip, n, q, "-z"]

    def generate_server_command(self, params):
        """Generate JackTrip command"""

        n = "-n" + params["channels"]
        q = "-q" + params["queue"]

        return ["jacktrip", "-s", n, q, "-z"]

    def start(self, params, p2p=False, server=False, peer_address=None):
        """Start JackTrip with relevent parameters"""

        command = self.generate_client_command(params, p2p, peer_address)
        if server is True:
            command = self.generate_server_command(params)
        self.current_jacktrip = Popen(command, stdout=PIPE, stderr=STDOUT)

    def stop(self):
        """Stop JackTrip"""

        self.current_jacktrip.terminate()
        self.current_jacktrip.wait()
