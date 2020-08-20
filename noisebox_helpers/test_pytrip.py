from pytrip import PyTrip
import configparser as cp
cfg = cp.ConfigParser(interpolation=cp.ExtendedInterpolation())
cfg.read('../config.ini')

def test_generate_command():
    session_params = {
        'hub_mode': cfg.get('jacktrip-default', 'hub_mode'),
        'server': cfg.get('jacktrip-default', 'server'),
        'ip': "123.123.123.123",
        'channels': cfg.get('jacktrip-default', 'channels'),
        'queue': cfg.get('jacktrip-default', 'queue')
        }
    mytrip = PyTrip()
    assert mytrip.generate_command(session_params) == ["jacktrip", "-C", "123.123.123.123", "-n1", "-q6", "-z"]
