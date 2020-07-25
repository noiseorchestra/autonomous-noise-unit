import subprocess
import psutil


def start(command):
    """Start JACK with relavent parameters"""
    subprocess.Popen(command)


def stop():
    """Stop JACK"""
    for proc in psutil.process_iter():
        if proc.name() == "jackd":
            proc.kill()


def get_input_port_names(jackClient):
    ports = jackClient.get_ports(is_audio=True, is_output=True)
    port_names = []
    for port in ports:
        port_names.append(port.name)
    return port_names
