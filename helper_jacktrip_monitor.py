from queue import Queue
from threading import Thread


class JacktripMonitor():
    """Helper object for monitoring stdout of jacktrip process"""

    def __init__(self, jacktrip):
        self.jacktrip = jacktrip
        self.queue = Queue()
        self._running = True

    def monitor(self, out_q):
        """Monitor jacktrip stdout and push to queue"""

        print("JackTrip monitor start")

        while self._running:
            out = str(self.jacktrip.stdout.readline().rstrip(), 'utf-8')
            print(out)
            out_q.put(out)

        print("JackTrip monitor should stop")

    def run(self):
        """Run monitor thread"""
        self.monitor_thread = Thread(target=self.monitor, args=(self.queue,))
        self.monitor_thread.start()

    def terminate(self):
        self._running = False
