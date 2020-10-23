import noisebox_helpers as nh


peers = [nh.peers.Ping(1, "peer01.peer"), nh.peers.Ping(0, "peer02.peer"), nh.peers.Ping(0, "peer03.peer"), nh.peers.Ping(1, "peer04.peer")]

def test_who_is_awake():
    assert nh.peers.who_is_awake(peers) == ["peer02.peer", "peer03.peer"]
