import configparser as cp
import noisebox_helpers as nh


cfg = cp.ConfigParser(interpolation=cp.ExtendedInterpolation())
cfg.read('default-config.ini')

def test_generate_client_command_peer_session():
    session_params = {
        'hub_mode': cfg.get('jacktrip-default', 'hub_mode'),
        'server': cfg.get('jacktrip-default', 'server'),
        'ip': "123.123.123.123",
        'jacktrip-channels': cfg.get('jacktrip-default', 'jacktrip-channels'),
        'queue': cfg.get('jacktrip-default', 'queue')
        }
    mytrip = nh.PyTrip()
    result = ["jacktrip", "-c", "234.234.234.234", "-n2", "-q6", "-z"]
    assert mytrip.generate_client_command(session_params,
                                   p2p=True,
                                   peer_address="234.234.234.234") == result

def test_generate_client_command_hub_server_session():
    session_params = {
        'hub_mode': cfg.get('jacktrip-default', 'hub_mode'),
        'server': cfg.get('jacktrip-default', 'server'),
        'ip': "123.123.123.123",
        'jacktrip-channels': cfg.get('jacktrip-default', 'jacktrip-channels'),
        'queue': cfg.get('jacktrip-default', 'queue')
        }
    mytrip = nh.PyTrip()
    result = ["jacktrip", "-C", "123.123.123.123", "-n2", "-q6", "-z"]
    assert mytrip.generate_client_command(session_params) == result

def test_generate_server_command():
    session_params = {
        'hub_mode': cfg.get('jacktrip-default', 'hub_mode'),
        'server': cfg.get('jacktrip-default', 'server'),
        'ip': "123.123.123.123",
        'jacktrip-channels': cfg.get('jacktrip-default', 'jacktrip-channels'),
        'queue': cfg.get('jacktrip-default', 'queue')
        }
    mytrip = nh.PyTrip()
    result = ["jacktrip", "-s", "-n2", "-q6", "-z"]
    assert mytrip.generate_server_command(session_params) == result
