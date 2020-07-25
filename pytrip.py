import subprocess
import psutil
import helper_jacktrip_monitor
import time


class PyTrip:
    """Helper object to start, monitor and disconnect JackTrip"""

    def __init__(self, params):
        print(params)
        self.ip = params["ip"]
        self.hub_mode = params["hub_mode"]
        self.server = params["server"]
        self.channels = "-n" + params["channels"]
        self.queue = "-q" + params["queue"]
        self.current_process = None
        self.jacktrip_monitor = None

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

        command = ' '.join(["jacktrip", mode, ip, self.channels, self.queue, "-z"])
        print(command)
        self.current_process = subprocess.Popen(command,
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE,
                                                shell=True)
        self.jacktrip_monitor = helper_jacktrip_monitor.JacktripMonitor(self.current_process, self.ip)
        self.jacktrip_monitor.run()
        while self.jacktrip_monitor.jacktrip_connected is False:
            time.sleep(0.5)

    def stop(self):
        """Stop JackTrip"""
        for proc in psutil.process_iter():
            if proc.name() == "jacktrip":
                proc.kill()

    # def monitor(self):
    #     """Monitor JackTrip startup and return connection status"""
    #     connected = False
    #     for line in iter(self.current_process.stdout.readline, b''):
    #         print(line.rstrip())
    #         if b'Received Connection from Peer!' in line.rstrip():
    #             print("jacktrip connected to: " + self.ip)
    #             connected = True
    #             break
    #
    #         if b'JackTrip Processes STOPPED!' in line.rstrip():
    #             print("Could not connect to: " + self.ip)
    #             print("JackTrip stopping")
    #             break
    #     print("After monitor loop")
    #     return connected
    #
    # def status(self):
    #     """Monitor JackTrip status and handle errors"""
    #     """...work in progress..."""
    #     for line in iter(self.current_process.stderr.readline, b''):
    #         print(line.rstrip())
    #         if b'UDP WAITED MORE THAN 10 seconds' in line.rstrip():
    #             print("jacktrip disconnected from: " + self.ip)
    #             yield False
    #         else:
    #             yield True
