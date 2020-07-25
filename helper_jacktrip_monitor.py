from queue import Queue
from threading import Thread
import oled_helpers
import time


class JacktripMonitor():

    def __init__(self, jacktrip, server_ip):
        self._sentinel = object()
        self.jacktrip = jacktrip
        self.jacktrip_connected = False
        self.jacktrip_error = False
        self.jacktrip_stopped = False
        self.server_ip = server_ip
        self.oled_helpers = oled_helpers.OLED_helpers()

    def producer(self, out_q):
        """Monitor jacktrip stdout and push to queue"""

        while self.jacktrip_stopped is not True:
            # Produce some data
            out = str(self.jacktrip.stdout.readline().rstrip(), 'utf-8')
            if out != '':
                out_q.put(out)

        # # Put the sentinel on the queue to indicate completion
        print("producer should stop")
        out_q.put(self._sentinel)

    # A thread that consumes data
    def consumer(self, in_q):
        """Check q messages"""

        while True:
            # Get some data
            data = in_q.get()

            # Check for termination
            if data is self._sentinel:
                in_q.put(self._sentinel)
                break

            # check q for error strings

            success = 'Received Connection from Peer!'
            stopped = 'JackTrip Processes STOPPED!'
            waiting = 'Waiting for Peer...'
            errors = ['Maybe the JACK server is not running',
                      'Unable to connect to JACK server',
                      'JACK server not running',
                      'Peer Buffer Size',
                      'Wrong bit resolution']

            print(data)

            if success in data:
                message = ['==SUCCESS==',
                           success,
                           'jacktrip connected to: ' + self.server_ip]
                print(message)
                self.oled_helpers.draw_lines(message)
                self.jacktrip_connected = True
                time.sleep(1)

            if waiting in data:
                message = ['==CONNECTING==',
                           waiting]
                print(message)
                self.oled_helpers.draw_lines(message)
                time.sleep(1)

            for error in errors:
                if error in data:
                    message = ['==ERROR==', error, 'JackTrip stopping']
                    self.oled_helpers.draw_lines(message)
                    self.jacktrip_connected = False
                    self.jacktrip_error = True
                    print(message)
                    time.sleep(1)

            if stopped in data:
                message = ['==ERROR==',
                           "Could not connect to: " + self.server_ip,
                           stopped]
                self.oled_helpers.draw_lines(message)
                self.jacktrip_connected = False
                self.jacktrip_error = True
                self.jacktrip_stopped = True
                print(message)
                time.sleep(1)

        print("consumer should stop")

    def run(self):
        """Run producer and consumer threads"""

        q = Queue()
        t1 = Thread(target=self.consumer, args=(q,))
        t2 = Thread(target=self.producer, args=(q,))
        t1.start()
        t2.start()
