from subprocess import Popen, PIPE
import psutil
import time
import jack
from itertools import product
from noisebox_helpers.custom_exceptions import NoiseBoxCustomError

class JackHelper:
    """Helper class for starting/stopping JACK, getting ports & managing connections"""

    def __init__(self):
        self.jackClient = None
        self.connections = []
        self.current_fpp = None

    def set_current_fpp(self, fpp):
        self.current_fpp = fpp

    def check_current_fpp(self, test_fpp):
        return test_fpp == self.current_fpp

    def generate_command(self, params):
        fpp = "256"
        if "jack-fpp" in params.keys():
            fpp = params["jack-fpp"]
        self.set_current_fpp(fpp)
        return ['jackd', '-R', '-dalsa', '-r48000', "-p" + fpp, '-n2', '-s', '-S']

    def start(self, params):
        """Start JACK with relavent parameters"""

        Popen(self.generate_command(params), stdout=PIPE, stderr=PIPE)
        time.sleep(2)
        self.jackClient = jack.Client('noisebox',  no_start_server=True)
        self.jackClient.activate()

    def stop(self):
        """Stop JACK"""

        for proc in psutil.process_iter():
            if proc.name() == "jackd":
                proc.kill()
                time.sleep(1)

    def check_input_ports(self, local_receive_ports, stereo):
        if len(local_receive_ports) == 0:
            raise NoiseBoxCustomError(["==ERROR==", "No audio inputs found"])

        if stereo is not True:
            local_receive_ports = [local_receive_ports[0]]

        return local_receive_ports

    def get_inputs(self, stereo):
        """Get an array of input port names"""

        local_receive_ports = self.jackClient.get_ports('system:capture.*')
        return self.check_input_ports(local_receive_ports, stereo)

    def get_jacktrip_receives(self):
        """Get an array of input port names"""

        return self.jackClient.get_ports('.*:receive.*')

    def is_already_connected(self, receive_port, send_port):
        """check if 2 ports are already connected"""

        connected_ports = self.jackClient.get_all_connections(receive_port)
        for connected_port in connected_ports:
            if send_port.name == connected_port.name:
                return True
        return False

    def connect(self, receive_port, send_port):
        """connect ports if not already connected"""

        if not self.is_already_connected(receive_port, send_port):
            self.jackClient.connect(receive_port, send_port)

    def set_all_connections(self, receive_ports_list, send_ports_list):
        """Connect a list of receive ports to a list of sends"""

        for connection in product(receive_ports_list, send_ports_list):
            print(connection)
            receive_ports = connection[0]
            send_ports = connection[1]

            receive_stereo = True if len(receive_ports) == 2 else False
            send_stereo = True if len(send_ports) == 2 else False

            self.connections.append((receive_ports[0], send_ports[0]))
            if receive_stereo and send_stereo:
                self.connections.append((receive_ports[1], send_ports[1]))
            elif receive_stereo and not send_stereo:
                self.connections.append((receive_ports[1], send_ports[0]))
            elif not receive_stereo and send_stereo:
                self.connections.append((receive_ports[0], send_ports[1]))

    def make_all_connections(self):
        [self.connect(c[0], c[1]) for c in self.connections]

    def disconnect_all(self, my_port):
        # from madwort py_patcher
        """disconnect everything from a port"""

        send_ports = self.jackClient.get_all_connections(my_port)
        for send_port in send_ports:
            print('disconnect', my_port.name, 'from', send_port.name)
            try:
                self.jackClient.disconnect(my_port, send_port)
            except Exception as e:
                print('error disconnecting, trying the other way round!', e)
                print('disconnect', send_port.name, 'from', my_port.name)
                self.jackClient.disconnect(send_port, my_port)
        self.connections = []

    def make_jacktrip_connections(self, stereo_input):
        """Make connections for jacktrip session"""

        self.disconnect_session()
        self.connections = []

        local_receive_ports = self.jackClient.get_ports('system:capture.*')
        local_send_ports = self.jackClient.get_ports('system:playback.*')
        jacktrip_send_ports = self.jackClient.get_ports(':send.*')
        # needs refactor to account for sessions with > 2 peers
        jacktrip_receive_ports = self.jackClient.get_ports(':receive.*')

        if stereo_input is not True:
            local_receive_ports = [local_receive_ports[0]]

        self.set_all_connections([local_receive_ports], [jacktrip_send_ports])
        self.set_all_connections([local_receive_ports], [local_send_ports])
        self.set_all_connections([jacktrip_receive_ports], [local_send_ports])
        self.make_all_connections()

    def make_monitoring_connections(self, stereo_input):
        """Make connections for monitoring local inputs"""

        local_receive_ports = self.jackClient.get_ports('system:capture.*')
        local_send_ports = self.jackClient.get_ports('system:playback.*')

        if stereo_input is not True:
            local_receive_ports = [local_receive_ports[0]]

        self.connections = []

        self.set_all_connections([local_receive_ports], [local_send_ports])
        self.make_all_connections()

    def disconnect_session(self):
        """Disconnect all ports from system playback"""

        for port in self.jackClient.get_ports('system:playback.*'):
            self.disconnect_all(port)
