from concurrent.futures import ThreadPoolExecutor
import subprocess
import time


class Ping:
    """Ping object to hold return values"""

    def __init__(self, rc, peer):
        self.rc = rc
        self.peer = peer


def ping_peer(peer):
    """Ping individual peer and return result"""

    process = subprocess.Popen(['ping', '-c', '1', peer])
    while process.poll() is None:
        time.sleep(0.5)

    rc = process.returncode
    ping_result = Ping(rc, peer)
    return ping_result


def ping_all(peers):
    """Check status of all peers and return result"""

    pool = ThreadPoolExecutor(20)
    pings = []
    results = []

    for peer in peers:
        thread = pool.submit(ping_peer, peer)
        pings.append(thread)

    for ping in pings:
        ping_result = ping.result()
        results.append(ping_result)

    return results


def get_online_peers(peers):
    """Run ping_all and return online peers"""

    peers = ping_all(peers)
    return who_is_awake(peers)


def who_is_awake(peers):
    return [peer.peer for peer in peers if peer.rc == 0]
