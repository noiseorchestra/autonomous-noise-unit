import subprocess
import time
from helper_jacktrip_monitor import JacktripMonitor
from helper_jacktrip_wait import JacktripWait


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
        self.jacktrip_monitor = None
        self.connected = False

    def start(self):
        """Start JackTrip with relevent parameters"""
        mode = ""
        ip = self.ip
        if self.hub_mode:
            mode = "-C"
        elif self.server:
            mode = "-s"
            ip = ""
        else:
            mode = "-c"

        command = ["jacktrip", mode, ip, self.channels, self.queue, "-z"]

        self.current_jacktrip = subprocess.Popen(command,
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.STDOUT)

        self.jacktrip_monitor = JacktripMonitor(self.current_jacktrip)
        self.jacktrip_monitor.run()

        jacktrip_wait = JacktripWait(self.ip, self.jacktrip_monitor)
        jacktrip_wait.run()

    def stop(self):
        """Stop JackTrip"""
        self.current_jacktrip.terminate()
        self.current_jacktrip.wait()
        self.jacktrip_monitor.terminate()
