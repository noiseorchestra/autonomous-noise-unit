from queue import Queue
from threading import Thread
from subprocess import Popen, PIPE


class ThreadedMeter:
    """Helper object for live monitoring the volume level of audio channels"""

    def __init__(self, command):
        self.current_meter_value = 0
        self.command = command
        self._sentinel = object()

    def producer(self, out_q, command):
        """Open process and push stdout to queue"""

        process = Popen(command, stdout=PIPE, shell=True)
        n = 0
        while n < 1000:
            # Produce some data
            line = process.stdout.readline().rstrip()
            out_q.put(line)
            n += 1
        process.terminate()
        # Put the sentinel on the queue to indicate completion
        out_q.put(self._sentinel)

    # A thread that consumes data
    def consumer(self, in_q):
        """Read and process level measurements from queue"""

        level = 0
        while True:
            # Get some data
            data = in_q.get()

            # Check for termination
            if data is self._sentinel:
                in_q.put(self._sentinel)
                break
            try:
                level = -2 * int(float(str(data, 'utf-8')))
            except TypeError:
                print("Meter value not int")
            finally:
                self.current_meter_value = level

        print('Consumer shutting down')

    def run(self):
        """Run producer and consumer threads"""

        q = Queue()
        t1 = Thread(target=self.consumer, args=(q,))
        t2 = Thread(target=self.producer, args=(q, self.command,))
        t1.start()
        t2.start()

    def get_current_value(self):
        return self.current_meter_value
