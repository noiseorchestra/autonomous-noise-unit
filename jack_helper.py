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
        ports = self.client.get_ports(is_audio=True, is_output=True)
        port_names = []
        for port in ports:
            port_names.append(port.name)
        return port_names

    def enable_monitoring(self):
        ports = self.client.get_ports(is_audio=True, is_output=True)
        for port in ports:
            self.disconnect_all(port)
        if len(ports) >= 2:
            self.client.connect(ports[0], 'system:playback_1')
            self.client.connect(ports[1], 'system:playback_2')
            connections1 = self.client.get_all_connections('system:playback_1')
            connections2 = self.client.get_all_connections('system:playback_2')
            print(connections1, connections2)
        elif len(ports) == 1:
            self.client.connect(ports[0], 'system:playback_1')
            self.client.connect(ports[0], 'system:playback_2')

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
