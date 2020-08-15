from queue import Queue
from threading import Thread


class PyTripMonitor():
    """Helper object for monitoring stdout of jacktrip process"""

    def __init__(self, jacktrip):
        self.jacktrip = jacktrip
        self.queue = Queue()
        self._running = True

    def monitor(self, out_q):
        """Monitor jacktrip stdout and push to queue"""

        while self._running:
            stdout = str(self.jacktrip.stdout.readline().rstrip(), 'utf-8')
            out_q.put(stdout)

    def run(self):
        """Run monitor thread"""
        self.monitor_thread = Thread(target=self.monitor, args=(self.queue,))
        self.monitor_thread.start()

    def terminate(self):
        self._running = False
