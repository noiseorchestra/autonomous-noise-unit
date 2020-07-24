from concurrent.futures import ThreadPoolExecutor
import subprocess
import time


class Ping:
    def __init__(self, rc, peer):
        self.rc = rc
        self.peer = peer
    pass


class Check_Peers:
    """Helper object to check status of peers"""

    def ping(self, peer):
        """Ping individual peer and return result"""
        process = subprocess.Popen(['ping', '-c', '1', peer])
        while process.poll() is None:
            # Process hasn't exited yet, let's wait some
            time.sleep(0.5)

        # Get return code from process
        rc = process.returncode
        ping_result = Ping(rc, peer)
        return ping_result

    def ping_all(self, peers):
        """Check status of all peers and return result"""
        pool = ThreadPoolExecutor(10)
        pings = []
        results = []

        for peer in peers:
            thread = pool.submit(self.ping, peer)
            pings.append(thread)

        for ping in pings:
            ping_result = ping.result()
            print(ping_result.peer, ' returned: ', ping_result.rc)
            results.append(ping_result)
        return results
