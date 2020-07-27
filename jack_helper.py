import subprocess
import psutil
import time
import jack


class JackHelper:

    def __init__(self, command):
        self.start(command)
        time.sleep(1)
        jackClient = jack.Client('noisebox',  no_start_server=True)
        jackClient.activate()

        self.client = jackClient

    def start(self, command):
        """Start JACK with relavent parameters"""

        subprocess.Popen(command)
        time.sleep(1)

    def stop(self):
        """Stop JACK"""

        for proc in psutil.process_iter():
            if proc.name() == "jackd":
                proc.kill()

    def get_input_port_names(self):
        """Get an array of input port names"""

        ports = self.client.get_ports(is_audio=True, is_output=True)
        port_names = []
        for port in ports:
            port_names.append(port.name)
        return port_names

    def connect_ports(self, receive_ports, send_ports_list):
        """Connect stereo/mono receive port/s to a list of send ports"""
        # if receive is stereo and send is mono only first channel is sent

        print('receive ports:', receive_ports)
        print('send ports:', send_ports_list)
        for receive_port in receive_ports:
            self.disconnect_all(receive_port)

        for send_ports in send_ports_list:
            for i, port in enumerate(send_ports):
                x = i
                if len(receive_ports) == 0:
                    continue
                if len(receive_ports) == 1:
                    x = 0
                self.client.connect(receive_ports[x], port)

    def disconnect_all(self, my_port):
        # from madwort py_patcher
        """disconnect everything from a port"""

        send_ports = self.client.get_all_connections(my_port)
        for send_port in send_ports:
            # do not disconnect from jack_capture ports
            # they do auto-reconnect, but the disconnection is not reliable
            print('disconnect', my_port.name, 'from', send_port.name)
            try:
                self.client.disconnect(my_port, send_port)
            except Exception as e:
                print('error disconnecting, trying the other way round!', e)
                print('disconnect', send_port.name, 'from', my_port.name)
                self.client.disconnect(send_port, my_port)

    def make_jacktrip_connections(self, ip):
        """Make connections for jacktrip session"""

        local_receive_ports = self.client.get_ports(is_audio=True,
                                                    is_output=True)
        local_send_ports = self.client.get_ports('system:playback.*')
        jacktrip_send_ports = self.client.get_ports(ip + ':send.*')
        jacktrip_receive_ports = self.client.get_ports(ip + ':receive.*')
        self.connect_ports(local_receive_ports, [jacktrip_send_ports,
                                                 local_send_ports])
        self.connect_ports(jacktrip_receive_ports, [local_send_ports])

    def make_monitoring_connections(self):
        """Make connections for monitoring local inputs"""

        local_receive_ports = self.client.get_ports(is_audio=True,
                                                    is_output=True)
        local_send_ports = self.client.get_ports('system:playback.*')
        self.connect_ports(local_receive_ports, [local_send_ports])

    def disconnect_session(self):
        """Disconnect all receive ports"""

        receive_ports = self.client.get_ports(is_audio=True, is_output=True)
        for port in receive_ports:
            self.disconnect_all(port)
