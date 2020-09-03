from pytrip import PyTrip
import configparser as cp
cfg = cp.ConfigParser(interpolation=cp.ExtendedInterpolation())
cfg.read('../config.ini')


def test_generate_client_command_peer_session():
    session_params = {
        'hub_mode': cfg.get('jacktrip-default', 'hub_mode'),
        'server': cfg.get('jacktrip-default', 'server'),
        'ip': "123.123.123.123",
        'jacktrip-channels': cfg.get('jacktrip-default', 'jacktrip-channels'),
        'queue': cfg.get('jacktrip-default', 'queue')
        }
    mytrip = PyTrip()
    result = ["jacktrip", "-c", "234.234.234.234", "-n1", "-q6", "-z"]
    assert mytrip.generate_client_command(session_params,
                                   p2p=True,
                                   peer_address="234.234.234.234") == result

def test_generate_client_command_hub_server_session():
    session_params = {
        'hub_mode': cfg.get('jacktrip-default', 'hub_mode'),
        'server': cfg.get('jacktrip-default', 'server'),
        'ip': "123.123.123.123",
        'jacktrip-channels': cfg.get('jacktrip-default', 'channels'),
        'queue': cfg.get('jacktrip-default', 'queue')
        }
    mytrip = PyTrip()
    result = ["jacktrip", "-C", "123.123.123.123", "-n1", "-q6", "-z"]
    assert mytrip.generate_client_command(session_params) == result

def test_generate_server_command():
    session_params = {
        'hub_mode': cfg.get('jacktrip-default', 'hub_mode'),
        'server': cfg.get('jacktrip-default', 'server'),
        'ip': "123.123.123.123",
        'jacktrip-channels': cfg.get('jacktrip-default', 'channels'),
        'queue': cfg.get('jacktrip-default', 'queue')
        }
    mytrip = PyTrip()
    result = ["jacktrip", "-s", "-n1", "-q6", "-z"]
    assert mytrip.generate_server_command(session_params) == result
