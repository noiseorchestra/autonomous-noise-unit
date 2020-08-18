from queue import Queue
from threading import Thread


class PyTripWatch():
    """Helper object for monitoring stdout of jacktrip process"""

    def __init__(self):
        self.queue = Queue()
        self._running = False

    def monitor(self, out_q, jacktrip):
        """Monitor jacktrip stdout and push to queue"""
        while self._running:
            try:
                stdout = str(jacktrip.stdout.readline().rstrip(), 'utf-8')
                out_q.put(stdout)
            except AttributeError as e:
                print("JackTrip stdout error: ", e)
                pass

    def run(self, jacktrip):
        """Run monitor thread"""
        self._running = True
        self.monitor_thread = Thread(target=self.monitor, args=(self.queue, jacktrip,))
        self.monitor_thread.start()

    def terminate(self):
        self._running = False
