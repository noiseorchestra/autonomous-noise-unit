from subprocess import Popen, PIPE, STDOUT
from helper_jacktrip_monitor import JacktripMonitor
from helper_jacktrip_wait import JacktripWait
from custom_exceptions import NoiseBoxCustomError

class PyTrip:
    """Helper object to start, monitor and disconnect JackTrip"""

    def __init__(self, params):
        print(params)
        self.ip = params["ip"]
        self.hub_mode = params["hub_mode"]
        self.server = params["server"]
        self.channels = "-n" + params["channels"]
        self.queue = "-q" + params["queue"]
        self.current_jacktrip = None
        self.connected = False

    def start(self):
        """Start JackTrip with relevent parameters"""

        command = ["jacktrip", "-C", self.ip, self.channels, self.queue, "-z"]

        self.current_jacktrip = Popen(command,
                                      stdout=PIPE,
                                      stderr=STDOUT)

        jacktrip_monitor = JacktripMonitor(self.current_jacktrip)
        jacktrip_monitor.run()

        jacktrip_wait = JacktripWait(self.ip, jacktrip_monitor)

        try:
            jacktrip_wait.run()
        except NoiseBoxCustomError:
            raise
        finally:
            jacktrip_monitor.terminate()
        # How to handle errors that occur later, during a session?

    def stop(self):
        """Stop JackTrip"""
        self.current_jacktrip.terminate()
        self.current_jacktrip.wait()
