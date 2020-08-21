from queue import Queue
from threading import Thread


class PyTripWatch():
    """Helper object for watchinging stdout of jacktrip process"""

    def __init__(self):
        self.queue = Queue()
        self._running = False

    def run(self, jacktrip):
        """Run watching in thread"""

        self.queue = Queue()
        self._running = True
        self.watching_thread = Thread(target=self.watch_jacktrip,
                                      args=(self.queue, jacktrip,))
        self.watching_thread.start()

    def watch_jacktrip(self, out_q, pytrip):
        """Monitor JackTrip stdout and push to queue"""

        while self._running:
            try:
                stdout = pytrip.current_jacktrip.stdout.readline()
                out_q.put(str(stdout.rstrip(), 'utf-8'))
            except AttributeError as e:
                print("JackTrip stdout error: ", e)
                pass

    def terminate(self):
        """Terminate watching thread"""

        self._running = False
        self.queue = Queue()
