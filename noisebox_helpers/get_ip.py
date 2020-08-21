import socket


def ip_address():
    """Get and return hostname & ip address"""

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = (s.getsockname()[0])
    sock_name = socket.gethostname()
    hostname = socket.gethostbyname(sock_name)
    s.close()
    print([sock_name, str(ip)])
    return [sock_name, hostname, str(ip)]
