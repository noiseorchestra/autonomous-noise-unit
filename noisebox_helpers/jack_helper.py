from subprocess import Popen, PIPE
import psutil
import time
import jack
import sys
from itertools import product
from noisebox_helpers.custom_exceptions import NoiseBoxCustomError

class JackHelper:

    def __init__(self, oled):
        self.oled = oled
        self.jackClient = None

    def start(self):
        """Start JACK with relavent parameters"""

        command = ['jackd', '-R', '-dalsa', '-r48000', '-p256', '-n2', '-s', '-S']
        Popen(command, stdout=PIPE, stderr=PIPE)
        time.sleep(1)

        try:
            self.jackClient = jack.Client('noisebox',  no_start_server=True)
        except Exception as e:
            print("JACK Client could not start", e)
            self.oled.draw_lines(["==ERROR==", "JACK didn't start", "Restarting script"])
            time.sleep(4)
            sys.exit("Exited because jackd not running")

        self.jackClient.activate()

    def stop(self):
        """Stop JACK"""

        for proc in psutil.process_iter():
            if proc.name() == "jackd":
                proc.kill()

    def get_input_port_names(self):
        """Get an array of input port names"""

        ports = self.jackClient.get_ports(is_audio=True, is_output=True)
        port_names = [port.name for port in ports]

        if len(port_names) == 0:
            raise NoiseBoxCustomError(["==ERROR==", "No audio inputs found"])

        return port_names

    def is_already_connected(self, receive_port, send_port):
        """check if 2 ports are already connected"""

        connected_ports = self.jackClient.get_all_connections(receive_port)
        for connected_port in connected_ports:
            if send_port == connected_port.name:
                return True
        return False

    def connect(self, receive_port, send_port):
        """connect ports if not already connected"""
        if not self.is_already_connected(receive_port, send_port):
            self.jackClient.connect(receive_port, send_port)

    def connect_all(self, receive_ports_list, send_ports_list):
        # create all possible connections between receive_ports and send_ports.
        for connection in product(receive_ports_list, send_ports_list):
            print(connection)
            receive_ports = connection[0]
            send_ports = connection[1]
            # don't connect a port to itself
            # if receive_ports[0].name.split(':')[0] == send_ports[0].name.split(':')[0]:
            #     continue

            # Make connections depending on stereo or mono clients
            receive_stereo = True if len(receive_ports) == 2 else False
            send_stereo = True if len(send_ports) == 2 else False

            if receive_stereo and send_stereo:
                self.connect(receive_ports[0], send_ports[0])
                self.connect(receive_ports[1], send_ports[1])
            if receive_stereo and not send_stereo:
                self.connect(receive_ports[0], send_ports[0])
                self.connect(receive_ports[1], send_ports[0])
            if not receive_stereo and send_stereo:
                self.connect(receive_ports[0], send_ports[0])
                self.connect(receive_ports[0], send_ports[1])
            if not receive_stereo and not send_stereo:
                self.connect(receive_ports[0], send_ports[0])

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

    def make_jacktrip_connections(self, ip, mono=True):
        """Make connections for jacktrip session"""

        local_receive_ports = self.jackClient.get_ports('system:capture.*')
        local_send_ports = self.jackClient.get_ports('system:playback.*')
        jacktrip_send_ports = self.jackClient.get_ports(ip + ':send.*')
        # needs refactor to account for sessions with > 2 peers
        jacktrip_receive_ports = self.jackClient.get_ports(ip + ':receive.*')

        self.disconnect_all(local_send_ports)

        if mono:
            local_receive_ports = [local_receive_ports[0]]

        self.connect_all([local_receive_ports], [jacktrip_send_ports, local_send_ports])
        self.connect_all([jacktrip_receive_ports], [local_send_ports])

    def make_monitoring_connections(self, mono=True):
        """Make connections for monitoring local inputs"""

        local_receive_ports = self.jackClient.get_ports('system:capture.*')
        local_send_ports = self.jackClient.get_ports('system:playback.*')

        if mono:
            local_receive_ports = [local_receive_ports[0]]

        self.connect_all([local_receive_ports], [local_send_ports])

    def disconnect_session(self):
        """Disconnect all receive ports"""

        for port in self.jackClient.get_ports('system:playback.*'):
            self.disconnect_all(port)
