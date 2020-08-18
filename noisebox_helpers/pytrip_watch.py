from queue import Queue
from threading import Thread


class PyTripWatch():
    """Helper object for watchinging stdout of jacktrip process"""

    def __init__(self):
        self.queue = Queue()
        self._running = False

    def watching(self, out_q, pytrip):
        """Monitor jacktrip stdout and push to queue"""
        while self._running:
            try:
                stdout = str(pytrip.current_jacktrip.stdout.readline().rstrip(), 'utf-8')
                out_q.put(stdout)
            except AttributeError as e:
                print("JackTrip stdout error: ", e)
                pass

    def run(self, jacktrip):
        """Run watching thread"""
        self._running = True
        self.watching_thread = Thread(target=self.watching,
                                      args=(self.queue, jacktrip,))
        self.watching_thread.start()

    def terminate(self):
        self._running = False
