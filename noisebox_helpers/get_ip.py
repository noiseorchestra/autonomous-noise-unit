import socket
import urllib.request

def ip_address():
    """Get and return hostname & ip address"""

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = (s.getsockname()[0])
    sock_name = socket.gethostname()
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    s.close()
    return [sock_name, external_ip, str(ip)]
