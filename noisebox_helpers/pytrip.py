from subprocess import Popen, PIPE, STDOUT
import noisebox_helpers as nh

class PyTrip:
    """Helper object to start, monitor and disconnect JackTrip"""

    def __init__(self):
        self.current_jacktrip = None
        self.connected = False
        self.pytrip_watch = nh.PyTripWatch()
        self.pytrip_wait = nh.PyTripWait()

    def generate_client_command(self, params, p2p=False, peer_address=None):
        """Generate JackTrip command"""

        ip = params["ip"] if p2p is not True else peer_address
        n = "-n" + params["jacktrip-channels"]
        q = "-q" + params["jacktrip-q"]
        server_type = "-C" if p2p is not True else "-c"

        return ["jacktrip", server_type, ip, n, q, "-z"]

    def generate_server_command(self, params):
        """Generate JackTrip command"""

        n = "-n" + params["jacktrip-channels"]
        q = "-q" + params["jacktrip-q"]

        return ["jacktrip", "-s", n, q, "-z"]

    def start(self, params, p2p=False, server=False, peer_address=None):
        """Start JackTrip with relevent parameters"""

        if server is True:
            command = self.generate_server_command(params)
        else:
            command = self.generate_client_command(params, p2p, peer_address)
        self.current_jacktrip = Popen(command, stdout=PIPE, stderr=STDOUT)

    def stop_watching(self):
        self.pytrip_watch.terminate()

    def stop(self):
        """Stop JackTrip"""

        self.current_jacktrip.terminate()
        self.current_jacktrip.wait()

    def connect_to_hub_server(self, session_params):
        """Start hubserver JackTrip session"""

        try:
            self.start(session_params)
        except Exception:
            self.stop()
            raise nh.NoiseBoxCustomError(["==JACKTRIP ERROR==", "JackTrip failed to start"])
        else:
            self.pytrip_watch.run(self)
            self.pytrip_wait.run(self.pytrip_watch, session_params['ip'])
            return {"connected": self.pytrip_wait.connected, "message": self.pytrip_wait.message}

    def connect_to_peer(self, session_params, server, peer_address):

        error_message = ["==JACKTRIP ERROR==", "JackTrip failed to start"]
        peer_address_or_server = "server"
        long_timeout = True

        if server is False:
            peer_address_or_server = peer_address
            long_timeout = False

        try:
            self.start(session_params, p2p=True, server=server, peer_address=peer_address)
        except Exception:
            self.stop()
            raise nh.NoiseBoxCustomError(error_message)
        else:
            self.pytrip_watch.run(self)
            self.pytrip_wait.run(self.pytrip_watch, peer_address_or_server, long_timeout=long_timeout)
            return {"connected": self.pytrip_wait.connected, "message": self.pytrip_wait.message}
