import noisebox_helpers as nh

dummy_cfg = {
    "jacktrip-default": {
        "ip": "123.123.123.123",
        "hub_mode": True,
        "server": False,
        "jacktrip-channels": "2",
        "input-channels": "2",
        "jacktrip-q": "6"

    }
}


def test_generate_client_command_peer_session():
    mytrip = nh.PyTrip()
    result = ["jacktrip", "-c", "234.234.234.234", "-n2", "-q6", "-z"]
    assert mytrip.generate_client_command(dummy_cfg["jacktrip-default"],
                                   p2p=True,
                                   peer_address="234.234.234.234") == result


def test_generate_client_command_hub_server_session():
    mytrip = nh.PyTrip()
    result = ["jacktrip", "-C", "123.123.123.123", "-n2", "-q6", "-z"]
    assert mytrip.generate_client_command(dummy_cfg["jacktrip-default"]) == result


def test_generate_server_command():
    mytrip = nh.PyTrip()
    result = ["jacktrip", "-s", "-n2", "-q6", "-z"]
    assert mytrip.generate_server_command(dummy_cfg["jacktrip-default"]) == result
